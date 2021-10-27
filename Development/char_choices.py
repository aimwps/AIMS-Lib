USER_STATUS =   (('deleted', 'deleted'),
                ('active', 'active'),
                ('inactive', 'inactive'),
                ('completed', 'completed'),
                )
RECORD_FREQUENCY =(
                    ('daily', 'Every day'),
                    ('weekly', 'Every week'),
                    ('monthly', 'Every month'),
                    ('yearly', 'Every year'),
                    ('custom', 'Specific days, weeks or months'),
                )
COMP_CRITERIA = (('consecutive', 'consecutive'),
                ('total', 'total'))
TRACKER_TYPE = (('maximize', 'Count Up'),
                ('minimize', 'Count Down'),
                ('boolean', 'Yes or No'),
                )
NUMBER_TYPE = (('float', 'Upto 2 decimal places'),
                ('integer', 'Whole number only'),
                )
CUSTOM_LOG_CODES =[
            ("Day repeat",
                        (
                            ("Monday", "Monday"),
                            ("Tuesday", "Tuesday"),
                            ("Wednesday", "Wendnesday"),
                            ("Thursday", "Thursday"),
                            ("Friday", "Friday"),
                            ("Saturday", "Saturday"),
                            ("Sunday", "Sunday")
                        )
            ),
            ("Day of month repeat",
                        (
                            ("1", 1),
                            ("2", 2),
                            ("3", 3),
                            ("4", 4),
                            ("5", 5),
                            ("6", 6),
                            ("7", 7),
                            ("8", 8),
                            ("9", 9),
                            ("10", 10),
                            ("11", 11),
                            ("12", 12),
                            ("13", 13),
                            ("14", 14),
                            ("15", 15),
                            ("16", 16),
                            ("17", 17),
                            ("18", 18),
                            ("19", 19),
                            ("20", 20),
                            ("21", 21),
                            ("22", 22),
                            ("23", 23),
                            ("24", 24),
                            ("25", 25),
                            ("26", 26),
                            ("27", 27),
                            ("28", 28),
                            ("29", 29),
                            ("30", 30),
                            ("31", 31),
                            ("last_day", "Last day in month")
                        )
            ),
            ("Month of year repeat",
                        (
                            ("January", "January"),
                            ("February", "February"),
                            ("March", "March"),
                            ("April", "April"),
                            ("May", "May"),
                            ("June", "June"),
                            ("July", "July"),
                            ("August", "August"),
                            ("September", "September"),
                            ("October", "October"),
                            ("November", "November"),
                            ("December", "December")
                        )
            )]
LOG_LENGTH = (("day", "A day"),
            ("week", "A week"),
            ("month", "A month"),
            ("year", "A year"))
