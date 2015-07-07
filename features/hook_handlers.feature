Feature: Hook handlers

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

      @hooks.before("/message > GET")
      def before_test(transaction):
          print("before hook handled")
          sys.stdout.flush()


      @hooks.after("/message > GET")
      def after_test(transaction):
          print("after hook handled")
          sys.stdout.flush()


      @hooks.before_validation("/message > GET")
      def before_validation(transaction):
          print("before validation hook handled")
          sys.stdout.flush()


      @hooks.before_all
      def before_all_test(transaction):
          print("before all hook handled")
          sys.stdout.flush()


      @hooks.after_all
      def after_all_test(transaction):
          print("after all hook handled")
          sys.stdout.flush()


      @hooks.before_each
      def before_each_test(transaction):
          print("before each hook handled")
          sys.stdout.flush()


      @hooks.before_each_validation
      def before_each_validation(transaction):
          print("before each validation hook handled")
          sys.stdout.flush()


      @hooks.after_each
      def after_each_test(transaction):
          print("after each hook handled")
          sys.stdout.flush()

      """

    When I run `dredd ./apiary.apib http://localhost:4567 --server "ruby server.rb" --language "dredd-hooks-python" --hookfiles ./hookfile.py`
    Then the exit status should be 0
    Then the output should contain:
      """
      before hook handled
      """
    And the output should contain:
      """
      before validation hook handled
      """
    And the output should contain:
      """
      after hook handled
      """
    And the output should contain:
      """
      before each hook handled
      """
    And the output should contain:
      """
      before each validation hook handled
      """
    And the output should contain:
      """
      after each hook handled
      """
    And the output should contain:
      """
      before all hook handled
      """
    And the output should contain:
      """
      after all hook handled
      """
