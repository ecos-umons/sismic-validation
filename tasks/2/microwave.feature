Feature: Basic microwave

  Background: Place an item into oven
    Given I open the door
    and I place an item in the oven
    and I close the door

  Scenario: Timer value is kept if door is opened then closed
    Given I press increase timer button 5 times
    and I open the door
    and I close the door
    and I press start button
    when 5 seconds elapsed
    then magnetron stops heating

  Scenario: Timer value is kept if door is opened then closed while cooking
    Given I press increase timer button 5 times
    and I press start button
    and 2 seconds elapsed
    when I open the door
    and I close the door
    and I press start button
    and 3 seconds elapsed
    then magnetron stops heating

  Scenario: Timer must be set to start cooking
    When I press start button
    then magnetron does not start heating

  Scenario: Timer must be greater than 0 to start cooking
    Given I press increase timer button
    and I press decrease timer button
    when I press start button
    then magnetron does not start heating

  Scenario Outline: Cooking time must correspond to timer
    Given I press increase timer button <time> times
    and I press start button
    when <seconds> seconds elapsed
    then magnetron stops heating

    Examples:
      | time | seconds |
      | 1    | 1       |
      | 2    | 2       |
      | 10   | 10      |
      | 50   | 50      |

  Scenario: Cooking time can be reset
    Given I press increase timer button 5 times
    and I press reset timer button
    and I press increase timer button 2 times
    and I press start button
    when 2 seconds elapsed
    then magnetron stops heating

  Scenario: Cooking time can be reset while cooking
    Given I press increase timer button 5 times
    and I press start button
    and 2 seconds elapsed
    when I press reset timer button
    then magnetron stops heating

  Scenario Outline: Timer can be increased while cooking
    Given I press increase timer button <initial> times
    and I press start button
    and <elapsed> seconds elapsed
    and I press increase timer button <additional> times
    when <remaining> seconds elapsed
    then magnetron stops heating

    Examples:
      | initial | elapsed | additional | remaining |
      | 10      | 6       | 1          | 5         |
      | 10      | 0       | 5          | 15        |
      | 10      | 6       | 5          | 9         |

  Scenario Outline: Timer can be decreased while cooking
    Given I press increase timer button <initial> times
    and I press start button
    and <elapsed> seconds elapsed
    and I press decrease timer button <substracted> times
    when <remaining> seconds elapsed
    then magnetron stops heating

    Examples:
      | initial | elapsed | substracted | remaining |
      | 10      | 6       | 1           | 3         |
      | 10      | 0       | 6           | 4         |
      | 10      | 6       | 3           | 1         |
      | 10      | 6       | 4           | 0         |
