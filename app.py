import typing

from piccolo.utils.pydantic import create_pydantic_model
from piccolo.engine import engine_finder

from blacksheep import Application, FromJSON, json, status_code

from bs_api.tables import Expense

app = Application()

ExpenseModelIn: typing.Any = create_pydantic_model(table=Expense, model_name=" ExpenseModelIn")

ExpenseModelOut: typing.Any = create_pydantic_model(table=Expense, include_default_columns=True, model_name=" ExpenseModelIn")

ExpenseModelPartial: typing.Any = create_pydantic_model(
    table=Expense, model_name="ExpenseModelPartial", all_optional=True
)

@app.router.get("/expenses")
async def expenses() -> typing.List[ExpenseModelOut]:
    return await Expense.select()

@app.router.get("/expense/{id}")
async def expense(id: int) -> typing.List[ExpenseModelOut]:
    expense = await Expense.select().where(id==Expense.id)
    if not expense:
        return json({}, status=status_code(404))
    return expense

@app.router.post("/expense")
async def create_expense(expense_model: FromJSON[ExpenseModelIn]) -> ExpenseModelOut:
    expense = Expense(**expense_model.value.dict())
    await expense.save()
    return ExpenseModelOut(**expense.to_dict())

@app.router.patch("expense/{id}")
async def patch_expense(
        id: int, expense_model: FromJSON[ExpenseModelPartial]
) -> ExpenseModelOut:
    expense = await Expense.objects().get(Expense.id == id)
    if not expense:
        return json({}, status = 404)

    for key, value in expense_model.value.dict().items():
        if value is not None:
            setattr(expense, key, value)

    await expense.save()
    return ExpenseModelOut(**expense.to_dict())


@app.router.put("/expenses/{id}")
async def put_expense(
        id: int, expense_model: FromJSON[ExpenseModelIn]
) -> ExpenseModelOut:
    expense = await Expense.objects().get(Expense.id == id)
    if not expense:
        return json({}, status = 404)

    for key, value in expense_model.value.dict().items():
        if value is not None:
            setattr(expense, key, value)

    await expense.save()
    return ExpenseModelOut(**expense.to_dict())

@app.router.delete("/expense/{id}")
async def delete_expense(id: int):
    expense = await Expense.objects().get(Expense.id == id)
    if not expense:
        return json({}, status=404)
    await expense.remove()
    return json({})

async def open_database_connection_pool(application):
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


async def close_database_connection_pool(application):
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")


app.on_start += open_database_connection_pool
app.on_stop += close_database_connection_pool