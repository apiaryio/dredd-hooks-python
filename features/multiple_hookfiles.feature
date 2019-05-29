Feature: Multiple hook files with a glob

  Background:
    Given I have Dredd installed
    And a file named "apiary.apib" with:
      """
      # My Api
      ## GET /message
      + Response 200 (text/plain)

              Hello World!
      """
    And a file "server.js" with a server responding on "http://localhost:4567/message" with "Hello World!"

  Scenario:
    Given a file named "hookfile1.py" with:
      """
      import dredd_hooks as hooks

      @hooks.before('/message > GET')
      def before(transaction):
          print("It's me, File1")
      """
    And a file named "hookfile2.py" with:
      """
      import dredd_hooks as hooks

      @hooks.before('/message > GET')
      def before(transaction):
          print("It's me, File2")
      """
    And a file named "hookfile_glob.py" with:
      """
      import dredd_hooks as hooks

      @hooks.before('/message > GET')
      def before(transaction):
          print("It's me, File3")
      """
    When I run `dredd ./apiary.apib http://localhost:4567 --server="node server.js" --language="dredd-hooks-python" --hookfiles=./hookfile1.py --hookfiles=./hookfile2.py --hookfiles=./hookfile_*.py --loglevel=debug`
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
