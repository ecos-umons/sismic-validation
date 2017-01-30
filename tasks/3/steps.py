from sismic.testing import steps
from behave import given, when, then, step


# General purpose
@step('I do "{scenario}"')
@step('scenario "{scenario}"')
def reproduce_scenario(context, scenario):
    steps.reproduce_scenario(context, scenario)


# Door
@step('I open the door')
def open_the_door(context):
    steps.send_event(context, 'door_opened')


@step('I close the door')
def close_the_door(context):
    steps.send_event(context, 'door_closed')


# Item
@step('I place an item in the oven')
def place_an_item(context):
    steps.send_event(context, 'item_placed')


@step('I remove the item from the oven')
def remove_the_item(context):
    steps.send_event(context, 'item_removed')


# Input - timer
@step('I press increase timer button')
@step('I press increase timer button {time:d} times')
def increase_cooking_duration(context, time=1):
    for i in range(time):
        steps.send_event(context, 'input_timer_inc')


@step('I press decrease timer button')
@step('I press decrease timer button {time:d} times')
def decrease_cooking_duration(context, time=1):
    for i in range(time):
        steps.send_event(context, 'input_timer_dec')


@step('I press reset timer button')
def reset_timer(context):
    steps.send_event(context, 'input_timer_reset')


# Input - power
@step('I press increase power button')
@step('I press increase power button {time:d} times')
def increase_power(context, time=1):
    for i in range(time):
        steps.send_event(context, 'input_power_inc')


@step('I press decrease power button')
@step('I press decrease power button {time:d} times')
def decrease_power(context, time=1):
    for i in range(time):
        steps.send_event(context, 'input_power_dec')


@step('I press reset power button')
def reset_power(context):
    steps.send_event(context, 'input_power_reset')


# Input - start/stop
@step('I press start button')
def start_button(context):
    steps.send_event(context, 'input_cooking_start')


@step('I press stop button')
def stop_button(context):
    steps.send_event(context, 'input_cooking_stop')


# Time related
@step('{seconds:d} seconds elapsed')
@step('{seconds:d} second elapsed')
def seconds_elapsed(context, seconds):
    for i in range(seconds):
        steps.send_event(context, 'timer_tick')


# Magnetron
@then('magnetron power is set to {power:d}W')
def magnetron_starts_with_power(context, power):
    return steps.event_is_received(context, 'heating_set_power', 'power', repr(power))


@then('magnetron power is not changed')
def magnetron_power_is_not_changed(context):
    return steps.event_is_not_received(context, 'heating_set_power')


@then('magnetron starts heating')
def magnetron_starts_heating(context):
    return steps.event_is_received(context, 'heating_on')


@then('magnetron does not start heating')
def magnetron_does_not_start_heating(context):
    return steps.event_is_not_received(context, 'heating_on')


@then('magnetron stops heating')
def magnetron_stops_heating(context):
    return steps.event_is_received(context, 'heating_off')


@then('magnetron does not stop heating')
def magnetron_does_not_stop_heating(context):
    return steps.event_is_not_received(context, 'heating_off')


# Lamp
@then('lamp turns on')
def lamp_turns_on(context):
    return steps.event_is_received(context, 'lamp_switch_on')


@then('lamp turns off')
def lamp_turns_off(context):
    return steps.event_is_received(context, 'lamp_switch_off')


@then('lamp does not turn off')
def lamp_stays_on(context):
    return steps.event_is_not_received(context, 'lamp_switch_off')


@then('lamp does not turn on')
def lamp_stays_off(context):
    return steps.event_is_not_received(context, 'lamp_switch_on')


# Turntable
@then('table starts turning')
def table_starts_turning(context):
    return steps.event_is_received(context, 'turntable_start')


@then('table stops turning')
def table_stops_turning(context):
    return steps.event_is_received(context, 'turntable_stop')


# Display & beep
@then('oven beeps once')
def oven_beeps_once(context):
    return steps.event_is_received(context, 'beep', 'number', 1)


@then('oven beeps {number:g} times')
def oven_beeps(context, number):
    return steps.event_is_received(context, 'beep', 'number', number)


@then('oven displays "{text}"')
def screen_displays(context, text):
    return steps.event_is_received(context, 'display_set', 'text', repr(text))


@then('oven display contains "{text}"')
def screen_displays(context, text):
    for event in context._events:
        if event.name == 'display_set':
            if text in getattr(event, 'text', ''):
                return
    assert False, '"{}" is not displayed'.format(text)


@then('oven display is cleared')
def screen_cleared(context):
    return steps.event_is_received(context, 'display_clear')
