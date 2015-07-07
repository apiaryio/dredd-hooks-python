Feature: Failing a transacstion

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
      import dredd_hooks as hooks

      @hooks.before("/message > GET")
      def before_test(transaction):
          transaction['fail'] = 'Yay! Failed!'

      """
    When I run `dredd ./apiary.apib http://localhost:4567 --server "ruby server.rb" --language "dredd-hooks-python" --hookfiles ./hookfile.py`
    Then the exit status should be 1
    And the output should contain:
      """
      Yay! Failed!
      """
