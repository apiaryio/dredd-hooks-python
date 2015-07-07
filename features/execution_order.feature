Feature: Execution order

  Background:
    Given I have "dredd-hooks-python" command installed
    And I have "dredd" command installed
    And a file named "server.rb" with:
      """
      require 'sinatra'
      get '/message' do
        "Hello World!\n\n"
      end
      """

    And a file named "apiary.apib" with:
      """
      # My Api
      ## GET /message
      + Response 200 (text/html;charset=utf-8)
          Hello World!
      """

  @debug
  Scenario:
    Given a file named "hookfile.py" with:
      """
      import sys
      import dredd_hooks as hooks

      key = 'hooks_modifications'

      @hooks.before("/message > GET")
      def before_test(transaction):
          transaction.setdefault(key, [])
          transaction[key].append("before modification")


      @hooks.after("/message > GET")
      def after_test(transaction):
          transaction.setdefault(key, [])
          transaction[key].append("after modification")


      @hooks.before_validation("/message > GET")
      def before_validation(transaction):
          transaction.setdefault(key, [])
          transaction[key].append("before validation modification")


      @hooks.before_all
      def before_all_test(transactions):
          transactions[0].setdefault(key, [])
          transactions[0][key].append("before all modification")

      @hooks.after_all
      def after_all_test(transactions):
          transactions[0].setdefault(key, [])
          transactions[0][key].append("after all modification")


      @hooks.before_each
      def before_each_test(transaction):
          transaction.setdefault(key, [])
          transaction[key].append("before each modification")


      @hooks.before_each_validation
      def before_each_validation(transaction):
          transaction.setdefault(key, [])
          transaction[key].append("before each validation modification")


      @hooks.after_each
      def after_each_test(transaction):
          transaction.setdefault(key, [])
          transaction[key].append("after each modification")

      """
    Given I set the environment variables to:
      | variable                       | value      |
      | TEST_DREDD_HOOKS_HANDLER_ORDER | true       |

    When I run `dredd ./apiary.apib http://localhost:4567 --server "ruby server.rb" --language "dredd-hooks-python" --hookfiles ./hookfile.py`
    Then the exit status should be 0
    Then the output should contain:
      """
      0 before all modification
      1 before each modification
      2 before modification
      3 before each validation modification
      4 before validation modification
      5 after modification
      6 after each modification
      7 after all modification
      """
