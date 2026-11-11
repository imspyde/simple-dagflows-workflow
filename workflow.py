from dataclasses import dataclass
from dagflows.authoring import Workflow
from dagflows.runtime import Ctx


wf = Workflow("expense-summery")

@dataclass
class Expense:
    item: str
    category: str
    amount_cents: int
    
@dataclass
class Expenses:
    expenses: list[Expense]
    

@dataclass
class Summery:
    count: int
    total_cents: int
    biggest_item: str
    by_category: dict[str, int]
    
@wf.node()
def collect_expenses(ctx: Ctx) -> Expenses:
    expenses = [
        Expense(item="Coffee", category="food", amount_cents=450),
        Expense(item="Groceries", category="food", amount_cents=6230),
        Expense(item="Buss Pass", category="transport", amount_cents=2500),
        Expense(item="Netflix", category="entertainment", amount_cents=1549),
        Expense(item="Refund", category="other", amount_cents=1000)
    ]
    ctx.log.info("Collected %d expenses", len(expenses))
    return Expenses(expenses=expenses)


@wf.node(depends=[collect_expenses])
def clean_expenses(batch: Expenses, ctx: Ctx) -> Expenses:
    kept = [e for e in batch.expenses if e.amount_cents >0]
    ctx.log.info("kept %d, dropped %d", len(kept), len(batch.expenses) - len(kept))
    return Expenses(expenses=kept)

@wf.node(depends=[clean_expenses])
def summarize(batch: Expenses, ctx: Ctx) -> Summery:
    by_category: dict[str, int] = {}
    for e in batch.expenses:
        by_category[e.category] = by_category.get(e.category, 0) + e.amount_cents
        
    biggest = max(batch.expenses, key = lambda e: e.amount_cents)
    summary = Summery(
        count=len(batch.expenses),
        total_cents=sum(by_category.values()),
        biggest_item=biggest.item,
        by_category=by_category
    )
        
    ctx.log.info(
            "Spent %d cents on %d items, biggest: %s",
            summary.total_cents,
            summary.count,
            summary.biggest_item
        )
    return summary