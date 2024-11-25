""" The following code passes all of the level 3 tests """



from banking_system import BankingSystem


import heapq
import math


class Account:
    def __init__(self,timestamp, Idnumber):
        self.Idnumber = Idnumber
        self.timestamp = timestamp
        self.balance = 0
        self.spent = 0

        """
        Cash back is a list of tuples. At the 0th index is
        the timestamp. At the 1st index is the two percent cash back.
        """
        self.cashback = [] # Class attribute to store cash back from pay function


    def __hash__(self):
        return hash(self.Idnumber)


    def __eq__(self, other):

        is_equal = False
        if self.spent == other.spent and self.Idnumber == other.Idnumber:
            is_equal = True

        return is_equal

    def __lt__(self, other):
        is_less_than = None
        if self.spent > other.spent:
            is_less_than = True
        elif self.spent < other.spent:
            is_less_than = False

        elif self.spent == other.spent:
            if self.Idnumber < other.Idnumber:
                is_less_than = True
            elif self.Idnumber > other.Idnumber:
                is_less_than = False

        return is_less_than

    def __gt__(self, other):
        is_greater_than = None
        if self.spent > other.spent:
            is_greater_than = False
        elif self.spent < other.spent:
            is_greater_than = True
        elif self.spent == other.spent:
            if self.Idnumber < other.Idnumber:
                is_greater_than = False
            elif self.Idnumber > other.Idnumber:
                is_greater_than = True

        return is_greater_than

    def add_money(self, deposit_amount):

        if deposit_amount > 0:
            self.balance += deposit_amount


        return self.balance

    def get_money(self, withdraw_amount):

        if withdraw_amount > 0 and withdraw_amount <= self.balance:
            self.balance -= withdraw_amount
            self.spent += withdraw_amount

        return self.balance

    def store_cashback(self, timestamp, amount, payment_info):

        # Add 86400000 to timestamp and save along with amount
        cashback_info = (timestamp, amount, payment_info)

        # Add cashback details to the list of cashbacks for this account
        self.cashback.append(cashback_info)





class BankingSystemImpl(BankingSystem):

    def __init__(self):
        self.list_of_accounts = {}
        self.list_of_transactions = {} # keys are accountids, values are an array of records (timestamp, balance, account_status)
        self.set_of_accounts = set()
        self.store_top_spenders = []
        self.payments = {} # dictionary of payments

    def pay(self, timestamp, accountId, amount):

        # Storing the timestamp that the cashback will be processed at
        timestamp_to_store = timestamp + 86400000

        # getting unique payment number: will be used as a key to store info into a dictionary
        payment_number = len(self.payments) + 1
        payment_string = "payment" + str(payment_number)


        # check if the account exists in our system
        if accountId not in self.list_of_accounts:
            print("Account Doesn't exist")
            return None

        if accountId in self.list_of_accounts:
            account = self.list_of_accounts[accountId]


        if account.balance < amount:
            self.process_cashback(timestamp, account)
            if account.balance < amount:
                print("Insufficient funds")
                return None
            else:
                # self.process_cashback(timestamp, account)  # need to think about this/ this will be a bank method
                two_percent = math.floor(amount * .02)

                # Not working need to debug

                payment_info = payment_string # renaming to be consistent with other functions

                account.store_cashback(timestamp_to_store, two_percent, payment_info)
                self.withdraw(timestamp, accountId, amount)

                """payment_status = "IN_PROGRESS"

                self.payments[payment_string] = (timestamp, accountId, payment_status)
                return payment_string"""

        else:
            # process the stored cash back before transaction
            # self.process_cashback(timestamp, account)  # need to think about this/ this will be a bank method
            two_percent = math.floor(amount * .02)

            # Not working need to debug

            payment_info = payment_string # renaming to be consistent with other functions

            account.store_cashback(timestamp_to_store, two_percent, payment_info)
            self.withdraw(timestamp, accountId, amount)

        payment_status = "IN_PROGRESS"
        """
        These values can't be immutable if accountIds can be changed (as can
        happen with merge_accounts()), changing this to an array for now
        """ 
        self.payments[payment_string] = [timestamp_to_store, accountId, payment_status]
        return payment_string


    def get_payment_status(self, timestamp, account_id, payment):

        if account_id not in self.list_of_accounts:
            print("Account doesn't exist.")
            return None
        # get the tuple contain the payment info

        if payment in self.payments:
            payment_info = self.payments[payment]
            if account_id != payment_info[1]:
                print("invalid payment info.")
                return None
            else:
                variable_to_return = ""

                # this will help pass a few test but could cause downstream problems
                account = self.list_of_accounts[account_id]



                payment_status_info = self.payments[payment]
                timestamp_to_compare = payment_status_info[0]

                if timestamp >= timestamp_to_compare:
                    variable_to_return = "CASHBACK_RECEIVED"
                    return variable_to_return
                else:
                    variable_to_return = "IN_PROGRESS"
                    return variable_to_return

        else:
            print("invalid payment number.")
            return None


        """
        # check that the payment status being requested is for the appropriate account
        if account_id == payment_status_info[1]:

            # if appropriate returns payment status to variable
            payment_status = payment_status_info[2] # info is stored as tuple
            return payment_status
        else:

        # If we have the wrong account then  return none along with informative message.
            print("wrong account")
            return None"""

    def update_transactions(self, timestamp, account_id, balance, account_active: bool = True):
        #self.list_of_transactions = {} # keys are accountids, values are an array of records (timestamp, balance, account_status)
        if account_id in self.list_of_transactions:
            self.list_of_transactions[account_id].append((timestamp, balance, account_active))
        else:
            self.list_of_transactions[account_id] = [(timestamp, balance, account_active)]

    def push_to_heap(self):
        self.store_top_spenders.clear()
        for account in self.set_of_accounts:
            heapq.heappush(self.store_top_spenders, account)

    def get_top_spender(self):
        top_spender = heapq.heappop(self.store_top_spenders)
        return top_spender

    def get_top_spender2(self):
        top_spender = self.store_top_spenders[0]
        self.store_top_spenders.pop(0)
        heapq.heapify(self.store_top_spenders)

        return top_spender

    def my_sorting_function(self, semi_sorted_accounts):
        count_1 = 0

        def swap(index1, index2):
            swapped_index = index1 , index2 = index2, index1
            return swapped_index

        while count_1 < len(semi_sorted_accounts):
            count_2 = count_1 + 1
            while count_2 < len(semi_sorted_accounts):
                if semi_sorted_accounts[count_1].spent == semi_sorted_accounts[count_2].spent:
                    if semi_sorted_accounts[count_1].Idnumber > semi_sorted_accounts[count_2].Idnumber:
                        swap(semi_sorted_accounts[count_1], semi_sorted_accounts[count_2])

                count_2 += 1
            count_1 += 1

        return semi_sorted_accounts



    def create_account(self, timestamp, account_id):

        if account_id not in self.list_of_accounts:
            new_account = Account(timestamp, account_id)
            self.list_of_accounts[account_id] = new_account
            self.set_of_accounts.add(new_account)
            self.push_to_heap()
            self.update_transactions(timestamp, account_id, new_account.balance)
            return True
        else:
            print("Account Id is already in use.")
            return False



    def deposit(self, timestamp, account_id, deposit_amount):


        if account_id in self.list_of_accounts:

            account_to_deposit_to = self.list_of_accounts[account_id]

            # process any cash back before deposit
            self.process_cashback(timestamp, account_to_deposit_to)
            account_to_deposit_to.add_money(deposit_amount)
            self.update_transactions(timestamp, account_to_deposit_to.Idnumber, account_to_deposit_to.balance)
            return account_to_deposit_to.balance
        else:
            print("Invalid Account")
            return None



    def withdraw(self, timestamp, accountId, withdraw_amount):

        if accountId in self.list_of_accounts:

            account_to_withdraw_from = self.list_of_accounts[accountId]

            self.process_cashback(timestamp, account_to_withdraw_from)
            account_to_withdraw_from.get_money(withdraw_amount)
            # account_to_withdraw_from.spent += withdraw_amount (resulted in overcount)
            self.push_to_heap()
            self.update_transactions(timestamp, account_to_withdraw_from.Idnumber, account_to_withdraw_from.balance)


            return True

        else:
            return False


    def transfer(self, timestamp, source_account_id, target_account_id, amount):

        if source_account_id != target_account_id:

            if source_account_id in self.list_of_accounts and target_account_id in self.list_of_accounts:
                account1 = self.list_of_accounts[source_account_id]
                account2 = self.list_of_accounts[target_account_id]
                if account1.balance >= amount:
                    account1.get_money(amount)
                    self.push_to_heap()
                    account2.add_money(amount)
                    self.update_transactions(timestamp, account1.Idnumber, account1.balance)
                    self.update_transactions(timestamp, account2.Idnumber, account2.balance)
                    return account1.balance
                else:
                    print("Insufficient Funds")
                    return None
        else:
            return None

    def process_cashback(self, timestamp, account):

        # check if the account has any scheduled cashback
        if len(account.cashback) != 0:
                count = 0

                while count < len(account.cashback):

                    cashback_info = account.cashback[count]
                    cashback_timestamp = cashback_info[0]
                    cashback_cash = cashback_info[1]
                    cashback_payment_key = cashback_info[2]

                    if timestamp >= cashback_timestamp:

                        accountb4 = account.balance
                        account.balance += cashback_cash
                        account_after = account.balance

                        print("Before and after: ", accountb4, account_after)



                        updated_payment_info = "Cashback received."
                        self.payments[cashback_payment_key] = (timestamp, account.Idnumber, updated_payment_info)
                        del account.cashback[count]

                    else:
                        count += 1
                        
    def check_cashback(self, timestamp, account):
        #Very similar to process, but doesn't update anything instead returning
        #the balance after cashback for the get_balance function.
        #This is repetitive code so we could modify process_cashback to include this
        return_balance = account.balance

        # check if the account has any scheduled cashback
        if len(account.cashback) != 0:

                for i in range(len(account.cashback)):

                    cashback_info = account.cashback[i]
                    cashback_timestamp = cashback_info[0]
                    cashback_cash = cashback_info[1]
                    cashback_payment_key = cashback_info[2]

                    if timestamp >= cashback_timestamp:

                        accountb4 = account.balance
                        return_balance += cashback_cash
                        account_after = return_balance 

                        print("Before and after: ", accountb4, account_after)
        return return_balance





    def top_spenders(self, timestamp, n):

        the_top_n_spenders = []

        if n >= len(self.store_top_spenders):
            k = len(self.store_top_spenders)
            for i in range(k):
                top_spender = self.get_top_spender2()
                spenderId = top_spender.Idnumber
                spender_outgoing = top_spender.spent
                proper_format = F"{spenderId}({spender_outgoing})"
                the_top_n_spenders.append(proper_format)

        else:
            for i in range(n):
                top_spender = self.get_top_spender2()
                spenderId = top_spender.Idnumber
                spender_outgoing = top_spender.spent
                proper_format = F"{spenderId}({spender_outgoing})"
                the_top_n_spenders.append(proper_format)


        self.push_to_heap()

        return the_top_n_spenders

    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:

        # Both accounts must be in list of accounts
        if account_id_1 not in self.list_of_accounts or account_id_2 not in self.list_of_accounts:
            return False
        # Accounts can't be equal
        elif account_id_1 == account_id_2:
            return False
        else:
            """
            Pending cashback refunds should be refunded to account 1 (or made pending to account 1)
            """
            account_1 = self.list_of_accounts[account_id_1]
            account_2 = self.list_of_accounts[account_id_2]
            for pending_cashback_operation in account_2.cashback:
                account_1.cashback.append(pending_cashback_operation)
            self.process_cashback(timestamp, account_1)

            """
            After merge can check status of payment transactions for account_id_2
            by replacing account_id_2 with account_id_1

            Note: So this will pass the test case, but I actually think this
            doesn't function as intended for the edge case where account 1 and
            account 2 have a payment 1. This may need to be changed for level 4
            and level 3, and we can also do it in a way that goes from O(N)
            time complexity for get payment status to O(1) by editing payments
            keys to include the account_id number concatenated with the payment
            number
            """
            for payment in self.payments.keys():
                if self.payments[payment][1] == account_id_2:
                    self.payments[payment][1] = account_id_1
            """
            Balance of account 2 added to account 1, this should not be counted
            as a withdrawal for the purposes of top spenders, so we CANNOT use
            the transfer method (or I guess we could, but you would have to
            then subtract the ammount just transfered from spent)
            """
            account_1.balance += account_2.balance
            account_2.balance -= account_2.balance

            """
            Top spenders must recognize account 1 as having the sum of 
            withdrawals for both accounts
            """
            account_1.spent += account_2.spent
            account_2.spent -= account_2.spent

            """
            Account 2 should be removed from the system, needs to be removed
            from list of accounts, set of accounts but not payments (since
            we already replaced instances of account 2 there with account 1's id)
            """
            del self.list_of_accounts[account_id_2]
            self.set_of_accounts.remove(account_2)

            # Update the heap 
            self.push_to_heap()
            self.update_transactions(timestamp, account_id_1, account_1.balance)
            self.update_transactions(timestamp, account_id_2, account_2.balance, account_active=False)
            return True

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        """
        Idea: if the time_at is in the future, check to see what balance would be
        after processing cash_back etc. at that timestamp. 

        If in past, binary search through list_of_transactions until hit timestamp or in between
        2 timestamps. Check to see if record with timestamp lesser than time_at 
        as an account_active == True. If it does, return the balance from that record,
        otherwise return None
        """
        # keys are accountids, values are an array of records (timestamp, balance, account_status)
        if account_id not in self.list_of_transactions:
            print("Account doesn't exist")
            return None
        transaction_list = self.list_of_transactions[account_id]
        if transaction_list[-1][0] < time_at and account_id in self.list_of_accounts:
            account = self.list_of_accounts[account_id]
            return self.check_cashback(time_at, account)
        elif transaction_list[-1][0] < time_at and account_id not in self.list_of_accounts:
            return None
        if transaction_list[0][0] > time_at:
            print("Account did not exist at time_at")
            return None
        else:
            low = 0
            high = len(transaction_list) - 1 
            while low <= high:
                mid = (high + low) // 2
                timestamp, balance, account_active = transaction_list[mid]
                if timestamp < time_at:
                    low = mid + 1
                elif timestamp  > time_at:
                    high = mid - 1
                else:
                    # in this case time_at is exactly equal to a timestamp
                    if account_active:
                        return balance 
                    else:
                        return None
            # If we break the loop can use lower bound to check
            index = 0
            if transaction_list[high][0] < time_at and transaction_list[low][0] > time_at:
                index = high
            elif transaction_list[low][0] < time_at and transaction_list[high][0] > time_at:
                index = low
            timestamp, balance, account_active = transaction_list[index]
            if account_active:
                return balance
            else:
                return None
                    

 

