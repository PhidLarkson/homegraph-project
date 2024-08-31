import {
  BillGenerated as BillGeneratedEvent,
  BillPaid as BillPaidEvent
} from "../generated/Contract/Contract"
import { BillGenerated, BillPaid } from "../generated/schema"

export function handleBillGenerated(event: BillGeneratedEvent): void {
  let entity = new BillGenerated(
    event.transaction.hash.concatI32(event.logIndex.toI32())
  )
  entity.user = event.params.user
  entity.amount = event.params.amount
  entity.billType = event.params.billType
  entity.dueDate = event.params.dueDate

  entity.blockNumber = event.block.number
  entity.blockTimestamp = event.block.timestamp
  entity.transactionHash = event.transaction.hash

  entity.save()
}

export function handleBillPaid(event: BillPaidEvent): void {
  let entity = new BillPaid(
    event.transaction.hash.concatI32(event.logIndex.toI32())
  )
  entity.user = event.params.user
  entity.amount = event.params.amount

  entity.blockNumber = event.block.number
  entity.blockTimestamp = event.block.timestamp
  entity.transactionHash = event.transaction.hash

  entity.save()
}
