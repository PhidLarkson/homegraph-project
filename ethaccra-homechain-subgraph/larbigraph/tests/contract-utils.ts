import { newMockEvent } from "matchstick-as"
import { ethereum, Address, BigInt } from "@graphprotocol/graph-ts"
import { BillGenerated, BillPaid } from "../generated/Contract/Contract"

export function createBillGeneratedEvent(
  user: Address,
  amount: BigInt,
  billType: i32,
  dueDate: BigInt
): BillGenerated {
  let billGeneratedEvent = changetype<BillGenerated>(newMockEvent())

  billGeneratedEvent.parameters = new Array()

  billGeneratedEvent.parameters.push(
    new ethereum.EventParam("user", ethereum.Value.fromAddress(user))
  )
  billGeneratedEvent.parameters.push(
    new ethereum.EventParam("amount", ethereum.Value.fromUnsignedBigInt(amount))
  )
  billGeneratedEvent.parameters.push(
    new ethereum.EventParam(
      "billType",
      ethereum.Value.fromUnsignedBigInt(BigInt.fromI32(billType))
    )
  )
  billGeneratedEvent.parameters.push(
    new ethereum.EventParam(
      "dueDate",
      ethereum.Value.fromUnsignedBigInt(dueDate)
    )
  )

  return billGeneratedEvent
}

export function createBillPaidEvent(user: Address, amount: BigInt): BillPaid {
  let billPaidEvent = changetype<BillPaid>(newMockEvent())

  billPaidEvent.parameters = new Array()

  billPaidEvent.parameters.push(
    new ethereum.EventParam("user", ethereum.Value.fromAddress(user))
  )
  billPaidEvent.parameters.push(
    new ethereum.EventParam("amount", ethereum.Value.fromUnsignedBigInt(amount))
  )

  return billPaidEvent
}
