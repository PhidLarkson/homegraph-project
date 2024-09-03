document.addEventListener('DOMContentLoaded', function () {
    const connectButton = document.getElementById('connect-metamask');
    const walletStatus = document.getElementById('wallet-status');
    const accountOverview = document.getElementById('account-overview');
    const payNowSection = document.getElementById('pay-now');
    let userAccount = null;
    let totalAmountDue = 0;

    // Function to connect to MetaMask
    async function connectMetaMask() {
        if (window.ethereum) {
            try {
                const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                userAccount = accounts[0];
                walletStatus.textContent = `>> ${userAccount}`;
                connectButton.disabled = true;
                fetchAndDisplayData();  // Fetch data once MetaMask is connected
            } catch (error) {
                console.error('User rejected the request:', error);
                walletStatus.textContent = 'Connection rejected!';
            }
        } else {
            console.error('MetaMask not detected!');
            walletStatus.textContent = 'MetaMask not detected!';
        }
    }

    connectButton.addEventListener('click', connectMetaMask);

    // Function to fetch and display data from the GraphQL API
    async function fetchAndDisplayData() {
        try {
            const graphqlEndpoint = "https://api.studio.thegraph.com/query/87752/larbigraph/version/latest";

            const billsGeneratedQuery = `
            {
                billGenerateds(first: 5) {
                    id
                    user
                    amount
                    billType
                    dueDate
                    blockNumber
                    blockTimestamp
                    transactionHash
                }
            }`;

            const billsPaidQuery = `
            {
                billPaids(first: 5) {
                    id
                    user
                    amount
                    blockNumber
                    blockTimestamp
                    transactionHash
                }
            }`;

            const billsGeneratedResponse = await axios.post(graphqlEndpoint, {
                query: billsGeneratedQuery
            });
            const billsPaidResponse = await axios.post(graphqlEndpoint, {
                query: billsPaidQuery
            });

            const billsGeneratedData = billsGeneratedResponse.data.data?.billGenerateds || [];
            const billsPaidData = billsPaidResponse.data.data?.billPaids || [];

            displayData('bills-generated', billsGeneratedData);
            displayData('bills-paid', billsPaidData);

            // Calculate and display the totals
            const totalGenerated = calculateTotal(billsGeneratedData);
            const totalPaid = calculateTotal(billsPaidData);

            displayAccountOverview(totalGenerated, totalPaid);

            // Calculate the total amount due
            totalAmountDue = totalGenerated - totalPaid;
            displayPayNowSection(totalAmountDue);

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    // Function to calculate the total amount from the data
    function calculateTotal(data) {
        return data.reduce((total, item) => total + parseFloat(item.amount), 0) / 1e18;  // Convert from Wei to ETH
    }

    // Function to display the account overview with totals
    function displayAccountOverview(totalGenerated, totalPaid) {
        accountOverview.innerHTML = `
            <p>Account: ${shortenText(userAccount)}</p>
            <p>Total Amount Generated: ${totalGenerated.toFixed(4)} ETH</p>
            <p>Total Amount Paid: ${totalPaid.toFixed(4)} ETH</p>
        `;
    }

    // Function to display the pay now section with the total amount due
    function displayPayNowSection(amountDue) {
        payNowSection.innerHTML = `
            <p>Total Amount Due: ${amountDue.toFixed(4)} ETH</p>
            <button id="pay-now-button" class="btn">Pay Now</button>
        `;

        const payNowButton = document.getElementById('pay-now-button');
        payNowButton.addEventListener('click', payNow);
    }

    // Function to handle payment using MetaMask
    async function payNow() {
        if (!userAccount || totalAmountDue <= 0) {
            alert("No payment due or MetaMask not connected.");
            return;
        }

        try {
            const transactionParams = {
                from: userAccount,
                to: '',  // fix with the actual recipient address
                value: (totalAmountDue * 1e18).toString(16),  // Convert ETH to Wei
                gasLimit: '0x5028',
                maxPriorityFeePerGas: '0x3b9aca00',
                maxFeePerGas: '0x2540be400',
            };

            const txHash = await ethereum.request({
                method: 'eth_sendTransaction',
                params: [transactionParams],
            });

            console.log('Transaction Hash:', txHash);
            alert('Payment successful! Transaction Hash: ' + txHash);
        } catch (error) {
            console.error('Payment failed:', error);
            alert('Payment failed. Please try again.');
        }
    }

    // Function to display data in a table format with shortened addresses and copy buttons
    function displayData(elementId, data) {
        const container = document.getElementById(elementId);
        container.innerHTML = '';  // Clear existing content

        if (data.length === 0) {
            container.innerHTML = '<p>No data available.</p>';
            return;
        }

        // Create the table element
        const table = document.createElement('table');
        table.className = 'data-table';

        // Create the table headers
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>ID</th>
                <th>User</th>
                <th>Amount</th>
                ${data[0].billType !== undefined ? '<th>Bill Type</th>' : ''}
                ${data[0].dueDate !== undefined ? '<th>Due Date</th>' : ''}
                <th>Block Number</th>
                <th>Block Timestamp</th>
                <th>Transaction Hash</th>
            </tr>
        `;
        table.appendChild(thead);

        // Create the table body
        const tbody = document.createElement('tbody');

        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${shortenText(item.id)} ${createCopyButton(item.id)}</td>
                <td>${shortenText(item.user)} ${createCopyButton(item.user)}</td>
                <td>${item.amount / 1e18} ETH</td>
                ${item.billType !== undefined ? `<td>${item.billType}</td>` : ''}
                ${item.dueDate !== undefined ? `<td>${new Date(parseInt(item.dueDate) * 1000).toLocaleString()}</td>` : ''}
                <td>${item.blockNumber}</td>
                <td>${new Date(parseInt(item.blockTimestamp) * 1000).toLocaleString()}</td>
                <td>${shortenText(item.transactionHash)} ${createCopyButton(item.transactionHash)}</td>
            `;
            tbody.appendChild(row);
        });

        table.appendChild(tbody);
        container.appendChild(table);
    }

    // Function to shorten text (e.g., hashes, addresses) for display
    function shortenText(text) {
        return `${text.slice(0, 4)}...${text.slice(-4)}`;
    }

    // Function to create a copy button
    function createCopyButton(text) {
        const copyButton = document.createElement('button');
        copyButton.textContent = '📋'; // You can use a different icon or text
        copyButton.style.marginLeft = '8px';
        copyButton.style.cursor = 'pointer';

        copyButton.addEventListener('click', () => {
            navigator.clipboard.writeText(text).then(() => {
                alert('Copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        });

        return copyButton.outerHTML; // Return the button as HTML string
    }
});
