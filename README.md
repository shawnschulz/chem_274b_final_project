# Chem_274b_final_project

## Overview:
This project implements a simplified version of a banking system, supporting various operations across multiple levels of complexity. The system comprises operations to handle the creation of new accounts, deposit money, transfer funds between accounts, rank according to top spenders, schedule payments with cashback, and merge accounts while retaining their account balances and transaction histories. Each transaction is time-stamped to track and ensure unique and strictly increasing order of operations. For successful implementation, the code was developed in increasing levels of complexity, (levels 1 - 4), progressively building on the previous functionality, and was tested across a series of tests at each level. All code is developed within the `banking_system_impl.py` file, using the provided boilerplate in `banking_system.py`.

## System Features:
- The system initializes by creating an Account Object. The Account has an `IDnumber`, `timestamp`, `balance`, `money spent`, and `cashback`.

- Users can deposit and withdraw by specifying the account, and the transaction. Each transaction is timestamped, and the account attributes are updated accordingly.

- The system is able to return the top spenders based on transaction history.

- After each payment transaction, accounts are eligible for a 2% cashback which gets applied to the balance 24 hours later.

- The system allows for the merging of accounts into a single account, while maintaining a historical record of all past transactions.

## Content:
- `banking_system_impl.py`: contains code implementation for the banking system that passes all tests in GradeScope.
- `banking_system.py`: Contains boilerplate code and instructions for implementation
- `Tests`: Contains test cases for each level of implementation.
- `UML Diagram`: Showcases the design methodology we followed to implement the code for level 1 - 2.

## Algorithmic Analysis (levels 1 & 2):

The following is a brief summary of the performance of each component of the project involved through level 2.
 
### Account Class:

- `Add money`:
	- Constant time O(1) 
	- This function does not depend on the size of the input.

- `Get money`:
	- Constant time O(1)
	- This function does not depend on the size of the input.

- `Overloaded operators =, <,  >`:
	- Constant time O(1)
	- This function does not depend on the size of the input.

- `StoreCashback`:
	- Constant time O(1)
	- This function does not depend on the size of their input.
		

### Bank Class:

- `push to heap`:
	- Logarithmic time O(logn)
	- This function uses a binary heap from heapq, which has a logarithmic push according to heapq documentation.
		
- `get top spender`:
	- Contains heap-pop which is O(logn)
	- This function uses a binary heap from heapq, which has a logarithmic pop according to heapq documentation.
	
- `create account`:
	- Constant time O(1)
	- This function searches through a dictionary and doesn’t depend on the size of the input.

- `Deposit`:
	- Linear time O(n) 
	- n is the number of times an account has paid money. The method calls process_cashback which loops over the list of pending cashback operations for an account, which in the worst case will be the size of the number of times the account has paid money.

- `Withdraw`:
	- Linear time O(n) 
	- n is the number of times an account has paid money. The method calls process_cashback which loops over the list of pending cashback operations for an account, which in the worst case will be the size of the number of times the account has paid money. Withdraw also calls push to heap which would add log(n) time complexity, but O(n + log(n) is equivalent to O(n).

- `Transfer`:
	- Logarithmic time O(logn)
	- This method involves pushing to a heap where n is the size of the heap.

- `Top spenders`:
	- Linearithmic time O(nlogn)
	- For the number (n) of top spenders requested (worst case n = number of accounts), you must pop from the heap which takes O(log n). Therefore, for each account, we have to pop from the heap resulting in linearithmic time.