import {
  assert,
  describe,
  test,
  clearStore,
  beforeAll,
  afterAll
} from "matchstick-as/assembly/index"
import { Address, BigInt } from "@graphprotocol/graph-ts"
import { BillGenerated } from "../generated/schema"
import { BillGenerated as BillGeneratedEvent } from "../generated/Contract/Contract"
import { handleBillGenerated } from "../src/contract"
import { createBillGeneratedEvent } from "./contract-utils"

// Tests structure (matchstick-as >=0.5.0)
// https://thegraph.com/docs/en/developer/matchstick/#tests-structure-0-5-0

describe("Describe entity assertions", () => {
  beforeAll(() => {
    let user = Address.fromString("0x0000000000000000000000000000000000000001")
    let amount = BigInt.fromI32(234)
    let billType = 123
    let dueDate = BigInt.fromI32(234)
    let newBillGeneratedEvent = createBillGeneratedEvent(
      user,
      amount,
      billType,
      dueDate
    )
    handleBillGenerated(newBillGeneratedEvent)
  })

  afterAll(() => {
    clearStore()
  })

  // For more test scenarios, see:
  // https://thegraph.com/docs/en/developer/matchstick/#write-a-unit-test

  test("BillGenerated created and stored", () => {
    assert.entityCount("BillGenerated", 1)

    // 0xa16081f360e3847006db660bae1c6d1b2e17ec2a is the default address used in newMockEvent() function
    assert.fieldEquals(
      "BillGenerated",
      "0xa16081f360e3847006db660bae1c6d1b2e17ec2a-1",
      "user",
      "0x0000000000000000000000000000000000000001"
    )
    assert.fieldEquals(
      "BillGenerated",
      "0xa16081f360e3847006db660bae1c6d1b2e17ec2a-1",
      "amount",
      "234"
    )
    assert.fieldEquals(
      "BillGenerated",
      "0xa16081f360e3847006db660bae1c6d1b2e17ec2a-1",
      "billType",
      "123"
    )
    assert.fieldEquals(
      "BillGenerated",
      "0xa16081f360e3847006db660bae1c6d1b2e17ec2a-1",
      "dueDate",
      "234"
    )

    // More assert options:
    // https://thegraph.com/docs/en/developer/matchstick/#asserts
  })
})
