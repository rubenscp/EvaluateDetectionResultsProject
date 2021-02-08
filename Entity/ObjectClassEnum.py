# Object Class enumerate


class ObjectClassEnum:

    def valueOf(className):
        if className == 'exuvia':
            return 0

        if className == 'instar1':
            return 1

        if className == 'instar2':
            return 2

        if className == 'instar3':
            return 3

        if className == 'instar4':
            return 4

        if className == 'adulta':
            return 5

        if className == 'ovo':
            return 6

        return 99

    def getValueName(classId):
        if classId == 0:
            return 'exuvia'

        if classId == 1:
            return 'instar1'

        if classId == 2:
            return 'instar2'

        if classId == 3:
            return 'instar3'

        if classId == 4:
            return 'instar4'

        if classId == 5:
            return 'adulta'

        if classId == 6:
            return 'exuvia'

        if classId == 7:
            return 'ovo'

        return ''
