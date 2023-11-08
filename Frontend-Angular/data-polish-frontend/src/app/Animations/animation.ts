import { trigger, animate, transition, style,query } from '@angular/animations';

export const fadeInAnimation =
    // trigger name for attaching this animation to an element using the [@triggerName] syntax
    trigger('fadeInAnimation', [

        // route 'enter' transition
        transition(':enter', [

            // css styles at start of transition
            style({ opacity: 0 ,
                transform: 'scale(0)'
            }),
            // style({
            //     position: 'absolute',
            //     left: 0,
            //     width: '100%',
            //     opacity: 0,
            //     transform: 'scale(0) translateY(10)',
            //   }),
            // animation and styles at end of transition
             animate('.5s ease-in-out', style({ opacity: 1,
                transform: 'scale(1)'
             }))
            //animate('60ms ease', style({ opacity: 1, transform: 'scale(1) translateY(0)' })),
        ]),
    ]);

   