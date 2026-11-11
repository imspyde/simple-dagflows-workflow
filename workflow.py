from dagflows.authoring import Workflow
from dagflows.runtime import Ctx


wf = Workflow("split-bill")


@wf.node()
def split_bill(ctx: Ctx) -> dict:
    bill = 2400        # the bill, in rupees
    tip_percent = 10   # the tip
    people = 4         # how many friends
 
    total = bill + bill * tip_percent / 100
    each = round(total / people, 2)
    
    ctx.log.info("total with tip: %.2f, each person pays: %.2f", total, each)
    return {"total": total, "each_pays": each}