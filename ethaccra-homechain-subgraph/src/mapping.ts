import { BigInt, Bytes } from '@graphprotocol/graph-ts'
import { BillGenerated, BillPaid, BillingContract } from '../generated/BillingContract/BillingContract'
import { BillGeneratedEntity, BillPaidEntity } from '../generated/schema'

// Handle BillGenerated event
export function handleBillGenerated(event: BillGenerated): void {
  let id = event.transaction.hash.toHex() + '-' + event.logIndex.toString()
  let billGenerated = new BillGeneratedEntity(id)

  billGenerated.user = event.params.user
  billGenerated.amount = event.params.amount
  billGenerated.billType = billTypeToString(event.params.billType)
  billGenerated.dueDate = event.params.dueDate
  billGenerated.timestamp = event.block.timestamp
  billGenerated.transactionHash = event.transaction.hash.toHex()

  billGenerated.save()
}

// Handle BillPaid event
export function handleBillPaid(event: BillPaid): void {
  let id = event.transaction.hash.toHex() + '-' + event.logIndex.toString()
  let billPaid = new BillPaidEntity(id)

  billPaid.user = event.params.user
  billPaid.amount = event.params.amount
  billPaid.timestamp = event.block.timestamp
  billPaid.transactionHash = event.transaction.hash.toHex()

  billPaid.save()
}

// Utility function to convert BillType enum to string
function billTypeToString(billType: i32): string {
  if (billType == 0) return 'Utility'
  if (billType == 1) return 'Rent'
  if (billType == 2) return 'Other'
  return 'Unknown'
}

// Handle fetching bill details (optional, not directly linked to events)
export function handleGetBillDetails(user: Bytes, billIndex: BigInt): void {
  let contract = BillingContract.bind(Address.fromString('YOUR_CONTRACT_ADDRESS'))
  let result = contract.getBillDetails(user, billIndex)

  // Handle the result if needed
  // result[0] - amount
  // result[1] - dueDate
  // result[2] - billType
  // result[3] - paid
}

// Handle fetching all bills for a user (optional, not directly linked to events)
export function handleGetBills(user: Bytes): void {
  let contract = BillingContract.bind(Address.fromString('YOUR_CONTRACT_ADDRESS'))
  let bills = contract.getBills(user)

  // Handle the list of bills if needed
}

// Handle paying a specific bill (optional, not directly linked to events)
export function handlePayBill(user: Bytes, billIndex: BigInt): void {
  let contract = BillingContract.bind(Address.fromString('YOUR_CONTRACT_ADDRESS'))
  contract.payBill(user, billIndex)

  // Additional logic or checks can be added if necessary
}

// Handle paying the latest bill (optional, not directly linked to events)
export function handlePayLatestBill(user: Bytes): void {
  let contract = BillingContract.bind(Address.fromString('YOUR_CONTRACT_ADDRESS'))
  let latestBillIndex = contract.getLatestBillIndex(user)

  contract.payBill(user, latestBillIndex)

  // Additional logic or checks can be added if necessary
}

// Handle paying a bill by amount (optional, not directly linked to events)
export function handlePayBillByAmount(user: Bytes, amount: BigInt): void {
  let contract = BillingContract.bind(Address.fromString('YOUR_CONTRACT_ADDRESS'))
  let billIndex = contract.findBillIndex(user, amount)

  contract.payBill(user, billIndex)

  // Additional logic or checks can be added if necessary
}

