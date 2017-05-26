import pyrekall.models.common
from pyrekall.models.processes import Process

class HiddenProc(Process):
    """
    This class is used to represent a Hidden Process
    """
    def __init__(self, eprocess, session):
        super(HiddenProc, self).__init__(eprocess, session)

        self.psActiveProcessHead = eprocess.obj_offset in session.GetParameter("pslist_psActiveProcessHead")
        self.csrss = eprocess.obj_offset in session.GetParameter("pslist_csrss")
        self.pspCidTable = eprocess.obj_offset in session.GetParameter("pslist_pspCidTable")
        self.sessions = eprocess.obj_offset in session.GetParameter("pslist_sessions")
        self.handles = eprocess.obj_offset in session.GetParameter("pslist_handles")
        self.psscan = eprocess.obj_offset in session.GetParameter("pslist_psscan")
        self.thrdproc = eprocess.obj_offset in session.GetParameter("pslist_thrdproc")

    def summary(self):
        summary = super(HiddenProc, self).summary()
        summary['psActiveProcessHead'] = self.psActiveProcessHead
        summary['csrss'] = self.csrss
        summary['pspCidTable'] = self.pspCidTable
        summary['sessions'] = self.sessions
        summary['handles'] = self.handles
        summary['psscan'] = self.psscan
        summary['thrdproc'] = self.thrdproc

        return summary