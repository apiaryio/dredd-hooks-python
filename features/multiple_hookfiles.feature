Feature: Multiple hookfiles with a glob

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

  Scenario:
    Given a file named "hookfile1.py" with:
      """
      import sys
      import dredd_hooks as hooks

      @hooks.before("/message > GET")
      def before_test(transaction):
          print("It's me, File1")
          sys.stdout.flush()

      """
    And a file named "hookfile2.py" with:
      """
      import sys
      import dredd_hooks as hooks

      @hooks.before("/message > GET")
      def before_test(transaction):
          print("It's me, File2")
          sys.stdout.flush()

      """
    And a file named "hookfile_to_be_globed.py" with:
      """
      import sys
      import dredd_hooks as hooks

      @hooks.before("/message > GET")
      def before_test(transaction):
          print("It's me, File3")
          sys.stdout.flush()

      """
    When I run `dredd ./apiary.apib http://localhost:4567 --server "ruby server.rb" --language "dredd-hooks-python" --hookfiles ./hookfile1.py --hookfiles ./hookfile2.py --hookfiles ./hookfile_*.py`
    Then the exit status should be 0
    And the output should contain:
      """
      It's me, File1
      """
    And the output should contain:
      """
      It's me, File2
      """
    And the output should contain:
      """
      It's me, File3
      """