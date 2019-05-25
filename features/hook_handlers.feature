Feature: Hook handlers

  Background:
    Given I have "dredd-hooks-python" command installed
    And I have "dredd" command installed
    And a file named "server.js" with:
      """
      require('http')
        .createServer((req, res) => {
          if (req.url === '/message') {
            res.writeHead(200, { 'Content-Type': 'text/plain' });
            res.end('Hello World!\n');
          } else {
            res.writeHead(500);
            res.end();
          }
        })
        .listen(4567);
      """

    And a file named "apiary.apib" with:
      """
      # My Api
      ## GET /message
      + Response 200 (text/plain)

              Hello World!
      """

  Scenario:
    Given a file named "hookfile.py" with:
      """
      import dredd_hooks as hooks

      @hooks.before('/message > GET')
      def before(transaction):
          print('before hook handled')

      @hooks.after('/message > GET')
      def after(transaction):
          print('after hook handled')

      @hooks.before_validation('/message > GET')
      def before_validation(transaction):
          print('before validation hook handled')

      @hooks.before_all
      def before_all(transaction):
          print('before all hook handled')

      @hooks.after_all
      def after_all(transaction):
          print('after all hook handled')

      @hooks.before_each
      def before_each(transaction):
          print('before each hook handled')

      @hooks.before_each_validation
      def before_each_validation(transaction):
          print('before each validation hook handled')

      @hooks.after_each
      def after_each(transaction):
          print('after each hook handled')
      """

    When I run `dredd ./apiary.apib http://localhost:4567 --server="node server.js" --language="dredd-hooks-python" --hookfiles=./hookfile.py --loglevel=debug`
    Then the exit status should be 0
    And the output should contain:
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
