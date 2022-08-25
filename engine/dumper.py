from engine.event import Event
from engine.place import Place


def dump_event(event: Event, is_else, condition_description, level=1):
    else_msg = 'Else ' if is_else else ''
    print(('\t' * level) + else_msg + event.str(condition_description))
    for item in event.inventory_items:
        print(('\t' * (level + 1)) + f'Item: {item}')

    for event in event.else_events:
        dump_event(event, True, condition_description, level + 1)

    for event in event.chained_events:
        dump_event(event, False, condition_description, level + 1)


def dump_place(condition_description, place: Place, explored: list[Place]):
    explored.append(place)
    print(place)

    for event in place.events:
        dump_event(event, False, condition_description)

    for item in place.inventory_items:
        print(f'\tItem: {item}')

    for transition in place.transitions:
        print(f'\tTransition: {transition}')

    for activity in place.activities:
        print(f'\tActivity: {activity}')

    for transition in place.transitions:
        if transition.place not in explored:
            explored.append(transition.place)
            dump_place(condition_description, transition.place, explored)
