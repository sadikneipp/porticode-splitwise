from flask import Flask, request, jsonify
from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import ExpenseUser

app = Flask(__name__)

session = {}
consumer_key = "8K5e87K3y5haqW8hmG6x6mbP8GeOwyFqoed01b6q"
consumer_secret = "pW2YnEoK7vuiNCyES5c6Rvj2iBo0z5xOaFfujm4L"
session['access_token'] = {'oauth_token': 'y5dvUvYXr5MO038WUBBpfCVKoYSMxHq7jQjHqGJG',
                           'oauth_token_secret': 'CyoxnwNMTi9sZ5BMD1ASl1r6e7Z9SRahLZq58lY6'}

sObj = Splitwise(consumer_key,
                 consumer_secret)
sObj.setAccessToken(session['access_token'])

@app.route('/splitwise/', methods=['GET', 'POST'])
def add_bill():
    data = request.get_json()
    cost = data['value']

    users = []
    group = sObj.getGroup(10204809)
    people = group.getMembers()

    expense = Expense()
    expense.setCost(str(cost))
    expense.setDescription("Capital One Transfer")
    # per_person = str(round(cost / len(people), 2))
    per_person = cost

    paying_user = sObj.getCurrentUser()
    paying_id = paying_user.getId()
    paying_expense_user = ExpenseUser()
    paying_expense_user.setId(paying_id)
    paying_expense_user.setPaidShare(str(cost))
    paying_expense_user.setOwedShare(per_person)
    users.append(paying_expense_user)

    for friend in people:
        id = friend.getId()
        if id == paying_id:
            continue
        user = ExpenseUser()
        user.setId(id)
        user.setPaidShare('0.0')
        user.setOwedShare(per_person)
        users.append(user)

    expense.setUsers(users)

    expense = sObj.createExpense(expense)
    print(expense.getId())
    return jsonify({'auth': 1})

@app.route('/splitwisebalance/', methods=['GET', 'POST'])
def check_owned_money():

    current_user = sObj.getCurrentUser()
    balance = current_user.getNetBalance()
    return jsonify({'value': balance})


# url, session['secret'] = sObj.getAuthorizeURL()
# @app.route('/')
# def splitwise():
#     oauth_token = request.args.get('oauth_token')
#     oauth_verifier = request.args.get('oauth_verifier')
#     session['access_token'] = sObj.getAccessToken(oauth_token, session['secret'], oauth_verifier)
#     sObj.setAccessToken(session['access_token'])

#     users = []

#     group = sObj.getGroup(10204809)
#     people = group.getMembers()

#     expense = Expense()
#     cost = 100.0
#     expense.setCost(str(cost))
#     expense.setDescription("Testing")
#     per_person = str(round(cost / len(people), 2))

#     paying_user =sObj.getCurrentUser()
#     paying_id = paying_user.getId()
#     paying_expense_user = ExpenseUser()
#     paying_expense_user.setId(paying_id)
#     paying_expense_user.setPaidShare(str(cost))
#     paying_expense_user.setOwedShare(per_person)
#     users.append(paying_expense_user)


#     for friend in people:
#         id = friend.getId()
#         if id == paying_id:
#             continue
#         user = ExpenseUser()
#         user.setId(id)
#         user.setPaidShare('0.0')
#         user.setOwedShare(per_person)
#         users.append(user)

#     expense.setUsers(users)

#     # expense = sObj.createExpense(expense)
#     print ('access_token: ' + str(session['access_token']))

#     return 'barambam bam'

# if __name__ == "__main__":
#     app.run(host='0.0.0.0')
