

STUDY_MODE_CHOICES = [
		('studied', 'STUDIED'),
		('unstudied', 'NOT STUDIED')
	]


SCHOOL_NOTICE_TYPE_CHOICES = [
			('school', 'ENTIRE SCHOOL'),
			('klass', 'CERTAIN CLASS'),
			('student', 'INDIVIDUAL STUDENT')
		]


SCHOOL_NOTICE_BOARD_STATUS_CHOICES = [
			('published', 'PUBLISHED'),
			('draft', "DRAFT"),
			('cancelled', 'CANCELLED')
		]


SCHOOL_STATUS_CHOICES = [
		('day', 'DAY'),
		('boarding', 'BOARDING')
	]

SCHOOL_TYPE_CHOICES = [
				('private', 'PRIVATE'),
				('public', 'PUBLIC'),
			]


PYSCHOMOTOR_CHOICES = (
    ('VERY_WEAK', 'Very Weak'),
    ('WEAK', 'Weak'),
    ('FAIR', 'Fair'),
    ('GOOD', 'Good'),
    ('EXCELLENT', 'Excellent')
)



TERM_CHOICES = (
    (1, 'First Term'),
    (2, 'Second Term'),
    (3, 'Third Term')
)

STATUS_CHOICES = (
    ('A', ('Active')),
    ('G', ('Graduated')),
    ('S', ('Suspended')),
    ('E', ('Expelled')),
    ('L', ('Left'))
)

SPECIAL_NEEDS = (
    ('Yes', 'Yes'),
    ('No', 'No')
)


SCHOOL_HEAD_REPORT_CARDS = [
			('a', 'Excellent Piece of Work Keep it up'),
			('b', 'Student can do better than this'),

		]


TEST_TYPE_CHOICES = (
    ('excercise', 'EXCERCISE'),
    ('test', 'TEST'),
    ('practice', 'PRACTICE'),
    ('exam', 'EXAM'),
)


ONLINE_ADMISSION_STATUS_CHOICES = [
		('pending', 'PENDING'),
		('approved', 'APPROVED'),
		('declined', 'DECLINED'),
		('meeting', 'REQUESTING A MEETING')
	]


ATTENDANCE_STATUS_CHOICES = [
				('present', 'PRESENT'),
				('absent', 'ABSENT'),
				('sick', 'SICK')
				('dismissed', 'DISMISSED'),
				('absconded', 'ABSCONDED')
			]


COURSES_STATUS_CHOICES = [
				('upcoming', 'UPCOMING'),
				('ongoing', 'ONGOING'),
				('finished', 'FINISHED'),
				('inactive', 'DE ACTIVATED'),

			]


STUDY_NOTES_STATUS_CHOICES = [
				('locked', 'LOCKED'),
				('unlocked', 'UNLOCKED'),
			]

STUDY_NOTES_APPROVAL_STATUS_CHOICES = [
				('approved', 'APPROVED'),
				('pending', 'PENDING APPROVAL'),
				('disapproved', 'DISAPPROVED'),

			]
















