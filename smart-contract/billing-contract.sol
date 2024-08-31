// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

contract BillingContract {
    enum BillType { Utility, Rent, Other }
    
    struct Bill {
        uint256 amount;
        uint256 dueDate;
        BillType billType;
        bool paid;
    }

    mapping(address => Bill[]) public bills;
    event BillGenerated(address indexed user, uint256 amount, BillType billType, uint256 dueDate);
    event BillPaid(address indexed user, uint256 amount);

    /**
     * @dev Generates a new bill for a user.
     * @param user The address of the user to generate a bill for.
     * @param amount The amount of the bill. Must be greater than zero.
     * @param billType The type of the bill.
     * @param dueDate The due date of the bill (timestamp).
     */
    function generateBill(address user, uint256 amount, BillType billType, uint256 dueDate) public {
        require(amount > 0, "Amount must be greater than zero");
        require(dueDate > block.timestamp, "Due date must be in the future");
        bills[user].push(Bill(amount, dueDate, billType, false));
        emit BillGenerated(user, amount, billType, dueDate);
    }

    /**
     * @dev Pays a specific bill for a user.
     * @param user The address of the user.
     * @param billIndex The index of the bill to pay.
     */
    function payBill(address user, uint256 billIndex) public {
        require(billIndex < bills[user].length, "Invalid bill index");
        Bill storage bill = bills[user][billIndex];
        require(!bill.paid, "Bill already paid");
        require(bill.amount > 0, "Bill amount should be greater than zero");
        require(block.timestamp <= bill.dueDate, "Cannot pay overdue bill"); // Optional: Allow payment of overdue bills
        bill.paid = true;
        emit BillPaid(user, bill.amount);
    }

    /**
     * @dev Checks if a bill is overdue.
     * @param user The address of the user.
     * @param billIndex The index of the bill.
     * @return bool indicating if the bill is overdue.
     */
    function isBillOverdue(address user, uint256 billIndex) public view returns (bool) {
        require(billIndex < bills[user].length, "Invalid bill index");
        Bill storage bill = bills[user][billIndex];
        return !bill.paid && block.timestamp > bill.dueDate;
    }

    /**
     * @dev Gets the details of a bill.
     * @param user The address of the user.
     * @param billIndex The index of the bill.
     * @return amount, dueDate, billType, paid status.
     */
    function getBillDetails(address user, uint256 billIndex) public view returns (uint256, uint256, BillType, bool) {
        require(billIndex < bills[user].length, "Invalid bill index");
        Bill storage bill = bills[user][billIndex];
        return (bill.amount, bill.dueDate, bill.billType, bill.paid);
    }

    // list bills
    function getBills(address user) public view returns (Bill[] memory) {
    return bills[user];
}

    // paying the latest bill
    function getLatestBillIndex(address user) public view returns (uint256) {
    uint256 length = bills[user].length;
    if (length > 0) {
        return length - 1;
    }
    revert("No bills available for this user");
}

    // pay a specific bill
    function findBillIndex(address user, uint256 amount) public view returns (uint256) {
    Bill[] memory userBills = bills[user];
    for (uint256 i = 0; i < userBills.length; i++) {
        if (userBills[i].amount == amount && !userBills[i].paid) {
            return i;
        }
    }
    revert("Bill not found");
}

    function payBillByAmount(address user, uint256 amount) public {
        uint256 billIndex = findBillIndex(user, amount);
        payBill(user, billIndex);
}


}
