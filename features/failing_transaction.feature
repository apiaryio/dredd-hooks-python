Feature: Failing a transaction

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
    Given a file named "hookfile.py" with:
      """
      import dredd_hooks as hooks

      @hooks.before('/message > GET')
      def before(transaction):
          transaction['fail'] = 'Yay! Failed!'
      """
    When I run `dredd ./apiary.apib http://localhost:4567 --server="node server.js" --language="dredd-hooks-python" --hookfiles=./hookfile.py --loglevel=debug`
    Then the exit status should be 1
    And the output should contain:
      """
      Yay! Failed!
      """
