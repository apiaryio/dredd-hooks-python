# -*- coding: utf-8 -*-
#
#  Copyright (c) 2015 Vilibald Wanča
#  License: MIT
#
import dredd_hooks as hooks
import sys

# *_all hooks
@hooks.before_all
def before_all_test(transactions):
    if 'hooks_modifications' not in transactions[0]:
        transactions[0]['hooks_modifications'] = []
    transactions[0]['hooks_modifications'].append("python before all mod")
    print('python before all hook')
    sys.stdout.flush()


@hooks.after_all
def after_all_test(transactions):
    print('YAY', file=sys.stderr)
    sys.stderr.flush()
    if 'hooks_modifications' not in transactions[0]:
        transactions[0]['hooks_modifications'] = []
    transactions[0]['hooks_modifications'].append("python after all mod")
    print('python after all hook')
    sys.stdout.flush()


# *_each hooks
@hooks.before_each
def before_each_test(transaction):
    if 'hooks_modifications' not in transaction:
        transaction['hooks_modifications'] = []
    transaction['hooks_modifications'].append("python before each mod")
    print('python before each hook')
    sys.stdout.flush()


@hooks.before_each_validation
def before_each_validation_test(transaction):
    if 'hooks_modifications' not in transaction:
        transaction['hooks_modifications'] = []
    transaction['hooks_modifications'].append("python before each validation mod")
    print('python before each validation hook')
    sys.stdout.flush()


@hooks.after_each
def after_each_test(transaction):
    if 'hooks_modifications' not in transaction:
        transaction['hooks_modifications'] = []
    transaction['hooks_modifications'].append("python after each mod")
    print('python after each hook')
    sys.stdout.flush()


# *_each hooks
@hooks.before_validation('Machines > Machines collection > Get Machines')
def before_validation_test(transaction):
    if 'hooks_modifications' not in transaction:
        transaction['hooks_modifications'] = []
    transaction['hooks_modifications'].append("python before validation mod")
    print('python before validation hook')
    sys.stdout.flush()


@hooks.before("Machines > Machines collection > Get Machines")
def before_test(transaction):
    if 'hooks_modifications' not in transaction:
        transaction['hooks_modifications'] = []
    transaction['hooks_modifications'].append("python before mod")
    print('python before hook')
    sys.stdout.flush()


@hooks.after('Machines > Machines collection > Get Machines')
def after_test(transaction):
    if 'hooks_modifications' not in transaction:
        transaction['hooks_modifications'] = []
    transaction['hooks_modifications'].append("python after mod")
    transaction['fail'] = 'Yay! Failed in python!'
    print('python after hook')
    sys.stdout.flush()
