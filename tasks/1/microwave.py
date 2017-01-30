import argparse
from functools import partial
from sismic.exceptions import ContractError
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter
from sismic.model import Event
from sismic.testing import ExecutionWatcher
import tkinter as tk
from tkinter import messagebox


####################################################

DISABLED_WIDGETS = [
    'w_input_power_inc',
    'w_input_power_dec',
    'w_input_power_reset',
    'w_display_frame',
    'w_turntable_frame',
    'w_heating_power',
    'w_input_cooking_stop',
    # For basic microwave:
    'w_item_placed',
    'w_item_removed',
    'w_lamp_frame',
    'w_weightsensor_frame',
]


# Create a tiny GUI
class MicrowaveApplication(tk.Frame):
    def __init__(self, master, statechart, contracts, properties):
        super().__init__(master)

        # Initialize widgets
        self.create_widgets()

        # Create a Stopwatch interpreter
        statechart = import_from_yaml(statechart)
        self.interpreter = Interpreter(statechart, ignore_contract=not contracts)

        # Bind interpreter events to the GUI
        self.interpreter.bind(self.event_handler)

        # Bind execution watchers
        self.watcher = ExecutionWatcher(self.interpreter)
        for prop in properties if properties else []:
            self.watcher.watch_with(import_from_yaml(prop), fails_fast=True)
        self.watcher.start()

        # Hide disabled widgets
        for widget_name in DISABLED_WIDGETS:
            widget = getattr(self, widget_name)
            widget.pack_forget()

        self.on_autotick()
        self.execute()

    def execute(self):
        try:
            print(self.interpreter.execute())
        except ContractError as e:
            messagebox.showerror(
                'Contract error!',
                e.__class__.__name__ + '\n\n' +
                'The following assertion does not hold in ' +
                str(e.obj) + ':\n' +
                e.condition + '\n\n' +
                'Step: \n' + str(e.step)
            )
            self.master.destroy()
            raise
        except AssertionError as e:
            messagebox.showerror('Unsatisfied property', e.args[0])
            self.master.destroy()
            raise
        except Exception as e:
            messagebox.showerror(
                'Fatal error',
                e.__class__.__name__ +
                ' was raised during the execution.\n' +
                'See console for the traceback.'
            )
            self.master.destroy()
            raise

        # Update the widget that contains the list of active states.
        self.w_states['text'] = '\n'.join(self.interpreter.configuration)

        self.w_context['text'] = '\n'.join(
            ['%s: %s' % (key, self.interpreter.context[key]) for key in sorted(self.interpreter.context)]
        )

    def create_widgets(self):
        self.pack(fill=tk.BOTH)

        # Statechart status
        controller_frame = tk.LabelFrame(self, text='CONTROLLER')
        controller_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=(8, 8))

        state_frame = tk.LabelFrame(controller_frame, text='Active configuration')
        state_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.w_states = tk.Label(state_frame)
        self.w_states.pack(side=tk.BOTTOM, fill=tk.X)

        context_frame = tk.LabelFrame(controller_frame, text='Context')
        context_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.w_context = tk.Label(context_frame)
        self.w_context.pack(side=tk.BOTTOM, fill=tk.X)

        #

        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        # Input frame
        input_frame = tk.LabelFrame(left_frame, text='INPUT BUTTONS')
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(8, 8))

        # Sensor frame
        sensors_frame = tk.LabelFrame(left_frame, text='ACTUATORS')
        sensors_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(8, 8))

        # Add buttons
        self.w_input_power_inc = tk.Button(input_frame, text='power +', command=partial(self.send_event, event_name='input_power_inc'))
        self.w_input_power_dec = tk.Button(input_frame, text='power -', command=partial(self.send_event, event_name='input_power_dec'))
        self.w_input_power_reset = tk.Button(input_frame, text='power 0', command=partial(self.send_event, event_name='input_power_reset'))

        self.w_input_timer_inc = tk.Button(input_frame, text='timer +', command=partial(self.send_event, event_name='input_timer_inc'))
        self.w_input_timer_dec = tk.Button(input_frame, text='timer -', command=partial(self.send_event, event_name='input_timer_dec'))
        self.w_input_timer_reset = tk.Button(input_frame, text='timer 0', command=partial(self.send_event, event_name='input_timer_reset'))

        self.w_input_cooking_start = tk.Button(input_frame, text='start', command=partial(self.send_event, event_name='input_cooking_start'))
        self.w_input_cooking_stop = tk.Button(input_frame, text='stop', command=partial(self.send_event, event_name='input_cooking_stop'))

        self.w_tick = tk.Button(sensors_frame, text='tick', command=partial(self.send_event, event_name='timer_tick'))
        self.v_autotick = tk.BooleanVar()
        self.v_autotick.set(True)
        self.w_autotick = tk.Checkbutton(sensors_frame, text='Auto-tick', var=self.v_autotick, command=self.on_autotick)

        self.w_item_placed = tk.Button(sensors_frame, text='place item', command=partial(self.send_event, event_name='item_placed'))
        self.w_item_removed = tk.Button(sensors_frame, text='remove item', command=partial(self.send_event, event_name='item_removed'))

        self.w_door_opened = tk.Button(sensors_frame, text='open door', command=partial(self.send_event, event_name='door_opened'))
        self.w_door_closed = tk.Button(sensors_frame, text='close door', command=partial(self.send_event, event_name='door_closed'))

        # Pack
        self.w_input_power_inc.pack(side=tk.TOP, fill=tk.X)
        self.w_input_power_dec.pack(side=tk.TOP, fill=tk.X)
        self.w_input_power_reset.pack(side=tk.TOP, fill=tk.X)

        self.w_input_timer_inc.pack(side=tk.TOP, fill=tk.X, pady=(8, 0))
        self.w_input_timer_dec.pack(side=tk.TOP, fill=tk.X)
        self.w_input_timer_reset.pack(side=tk.TOP, fill=tk.X)

        self.w_input_cooking_start.pack(side=tk.TOP, fill=tk.X, pady=(8, 0))
        self.w_input_cooking_stop.pack(side=tk.TOP, fill=tk.X)

        self.w_autotick.pack(side=tk.TOP, fill=tk.X)
        self.w_tick.pack(side=tk.TOP, fill=tk.X)

        self.w_item_placed.pack(side=tk.TOP, fill=tk.X, pady=(8, 0))
        self.w_item_removed.pack(side=tk.TOP, fill=tk.X)

        self.w_door_opened.pack(side=tk.TOP, fill=tk.X, pady=(8, 0))
        self.w_door_closed.pack(side=tk.TOP, fill=tk.X)

        right_frame = tk.LabelFrame(self, text='COMPONENTS')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(8, 8))

        # Door component
        self.w_doorsensor_frame = tk.LabelFrame(right_frame, text='Door')
        self.w_doorsensor_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.w_doorsensor = tk.Label(self.w_doorsensor_frame)
        self.w_doorsensor.config(text='closed')
        self.w_doorsensor.pack(side=tk.TOP)

        # Weightsensor component
        self.w_weightsensor_frame = tk.LabelFrame(right_frame, text='Weight sensor')
        self.w_weightsensor_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.w_weightsensor = tk.Label(self.w_weightsensor_frame)
        self.w_weightsensor.config(text='no item')
        self.w_weightsensor.pack(side=tk.TOP)

        # Display component
        self.w_display_frame = tk.LabelFrame(right_frame, text='Display')
        self.w_display_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.w_display = tk.Label(self.w_display_frame)
        self.w_display.pack(side=tk.TOP)

        # Lamp component
        self.w_lamp_frame = tk.LabelFrame(right_frame, text='Lamp')
        self.w_lamp_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.w_lamp = tk.Label(self.w_lamp_frame)
        self.w_lamp.pack(side=tk.TOP)

        # Heating component
        self.w_heating_frame = tk.LabelFrame(right_frame, text='Heating')
        self.w_heating_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.w_heating_power = tk.Label(self.w_heating_frame)
        self.w_heating_status = tk.Label(self.w_heating_frame)
        self.w_heating_power.pack(side=tk.TOP)
        self.w_heating_status.pack(side=tk.TOP)

        # Beeper component
        self.w_beep_frame = tk.LabelFrame(right_frame, text='Beeper')
        self.w_beep_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.w_beep = tk.Label(self.w_beep_frame)
        self.w_beep.pack(side=tk.TOP)

        # Turntable component
        self.w_turntable_frame = tk.LabelFrame(right_frame, text='Turntable')
        self.w_turntable_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.w_turntable = tk.Label(self.w_turntable_frame)
        self.w_turntable.pack(side=tk.TOP)

    def event_handler(self, event):
        name = event.name

        if name == 'lamp_switch_on':
            self.w_lamp['text'] = 'on'
        elif name == 'lamp_switch_off':
            self.w_lamp['text'] = 'off'
        elif name == 'display_set':
            self.w_display['text'] = event.text
        elif name == 'display_clear':
            self.w_display['text'] = ''
        elif name == 'heating_set_power':
            self.w_heating_power['text'] = event.power
        elif name == 'heating_on':
            self.w_heating_status['text'] = 'on'
        elif name == 'heating_off':
            self.w_heating_status['text'] = 'off'
        elif name == 'beep':
            self.w_beep['text'] = event.number
        elif name == 'turntable_start':
            self.w_turntable['text'] = 'on'
        elif name == 'turntable_stop':
            self.w_turntable['text'] = 'off'
        else:
            raise ValueError('Unknown event %s' % event)

    def on_autotick(self):
        if self.v_autotick.get():
            self.send_event('timer_tick')
            self.after(1000, self.on_autotick)

    def send_event(self, event_name):
        if event_name == 'item_placed':
            self.w_weightsensor.config(text='item detected')
        elif event_name == 'item_removed':
            self.w_weightsensor.config(text='no item')
        elif event_name == 'door_opened':
            self.w_doorsensor.config(text='open')
        elif event_name == 'door_closed':
            self.w_doorsensor.config(text='closed')
            
        self.interpreter.queue(Event(event_name))
        self.execute()

    def _quit(self):
        self.master.destroy()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Microwave GUI')
    parser.add_argument(
        'microwave',
        metavar='filepath',
        type=argparse.FileType('r'),
        help='Path to the YAML file that contains the microwave',
    )
    parser.add_argument(
        '--contracts',
        action='store_true',
        help='Enable contracts checking during execution',
    )
    parser.add_argument(
        '--properties',
        type=argparse.FileType('r'),
        metavar='PROPERTY',
        nargs='*',
        default=[],
        help='Path(s) to the file(s) that contain(s) property statechart(s)')

    args = parser.parse_args()

    # Create GUI
    root = tk.Tk()
    root.wm_title('Microwave')
    app = MicrowaveApplication(
        master=root,
        statechart=args.microwave,
        contracts=args.contracts,
        properties=args.properties
    )

    app.mainloop()
