Feature: Lamp

  Scenario: Lamp turns on when door is opened
    When I open the door
    then lamp turns on

  Scenario: Lamp turns off when door is closed
    Given I open the door
    when I close the door
    then lamp turns off

  Scenario: Lamp turns on when cooking starts
    Given I open the door
    and I place an item in the oven
    and I close the door
    and I press increase timer button 5 times
    when I press start button
    then lamp turns on

  Scenario: Lamp stays on when door is opened while cooking
    Given scenario "Lamp turns on when cooking starts"
    and 2 seconds elapsed
    when I open the door
    then lamp does not turn off

  Scenario: Lamp turns off when cooking time elapsed
    Given scenario "Lamp turns on when cooking starts"
    when 5 seconds elapsed
    then lamp turns off
