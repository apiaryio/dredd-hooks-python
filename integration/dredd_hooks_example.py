import dreddhooks as dredd

# *_all hooks
@dredd.before_all
def before_all_test(transactions):
    if 'hooks_modifications' not in transactions[0]:
        transactions[0]['hooks_modifications'] = []
    transactions[0]['hooks_modifications'].append("python before all mod")
    print('python before all hook')

@dredd.after_all
def after_all_test(transactions):
    if 'hooks_modifications' not in transactions[0]:
        transactions[0]['hooks_modifications'] = []
    transactions[0]['hooks_modifications'].append("python after all mod")
    print('python after all hook')

# *_each hooks
@dredd.before_each
def before_each_test(transaction):
    if 'hooks_modifications' not in transaction:
        transaction['hooks_modifications'] = []
    transaction['hooks_modifications'].append("python before each mod")
    print('python before each hook')

@dredd.before_each_validation
def before_each_validation_test(transaction):
    if 'hooks_modifications' not in transaction:
        transaction['hooks_modifications'] = []
    transaction['hooks_modifications'].append("python before each validation mod")
    print('python before each validation hook')

@dredd.after_each
def after_each_test(transaction):
    if 'hooks_modifications' not in transaction:
        transaction['hooks_modifications'] = []
    transaction['hooks_modifications'].append("python after each mod")
    print('python after each hook')

# *_each hooks
@dredd.before_validation('Machines > Machines collection > Get Machines')
def before_validation_test(transaction):
    if 'hooks_modifications' not in transaction:
        transaction['hooks_modifications'] = []
    transaction['hooks_modifications'].append("python before validation mod")
    print('python before validation hook')

@dredd.before("Machines > Machines collection > Get Machines")
def before_test(transaction):
    if 'hooks_modifications' not in transaction:
        transaction['hooks_modifications'] = []
    transaction['hooks_modifications'].append("python before mod")
    print('python before hook')

@dredd.after('Machines > Machines collection > Get Machines')
def after_test(transaction):
    if 'hooks_modifications' not in transaction:
        transaction['hooks_modifications'] = []
    transaction['hooks_modifications'].append("python after mod")
    print('python after hook')
    transaction['fail'] = 'Yay! Failed in python!'

