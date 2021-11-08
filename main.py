from machine import Pin, ADC
import utime
import time


sail_step = Pin(12)
sail_direction = Pin(13, Pin.OUT)

claw_step = Pin(17)
claw_direction = Pin(16, Pin.OUT)

lift_step = Pin(14)
lift_direction = Pin(15, Pin.OUT)

select_button = Pin(19, Pin.IN, Pin.PULL_DOWN)
direction_button = Pin(18, Pin.IN, Pin.PULL_DOWN)



# To control speed just modify the amount/value of nop[dely amount 0-31].
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def move():
    wrap_target()
    set(pins, 1)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    
    set(pins, 0)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    wrap()

"""Instantiate a state machine with the move
program, at 100000Hz, with set base to step pin."""
sail_motor = rp2.StateMachine(0, move, freq=50000,  set_base=sail_step)
lift_motor = rp2.StateMachine(1, move, freq=100000, set_base=lift_step)
claw_motor = rp2.StateMachine(2, move, freq=100000, set_base=claw_step)

# select = [sail, lift, claw] = [0,1,2]
select = 1
# direction = [off, forward, backward] = [0,1,2]
direction = 1

while True:
    
    if select_button.value():
        if select == 0:
            """Sail"""
            select = 1
            
        elif select == 1:
            """Lift"""
            select = 2
            
        elif select == 2:
            """Claw"""
            select = 0
            
        # Required so the button has time to reset.    
        time.sleep(0.5)
    
    if direction_button.value():
        if direction == 0:
            """Dont move"""
            sail_motor.active(0)
            lift_motor.active(0)
            claw_motor.active(0)
            direction = 1
            print(0)
              
        elif direction == 1:
            """forward"""
            # 1 In / 0 Out
            sail_direction.value(0)
            # 1 Down / 0 Up
            lift_direction.value(0)
            # 1 Close / 0 Open
            claw_direction.value(0)
            
            # Run the motors based on the one selected.
            if select == 0:
                """Sail"""
                sail_motor.active(1)
                print("Sail")
            elif select == 1:
                """Lift"""
                lift_motor.active(1)
                print("Lift")
            elif select == 2:
                """Claw"""
                claw_motor.active(1)
                print("claw")
            
            # Set next click
            direction = 2
            print(2)
            
        elif direction == 2:
            """Backward"""
            sail_direction.value(1)
            lift_direction.value(1)
            claw_direction.value(1)
            
            if select == 0:
                """Sail"""
                sail_motor.active(1)
            elif select == 1:
                """Lift"""
                lift_motor.active(1)       
            elif select == 2:
                """Claw"""
                claw_motor.active(1)
            direction = 0
            
            print(2)
        
        
        
            
        # Required so the button has time to reset.
        time.sleep(0.5)



