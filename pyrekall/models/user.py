import pyrekall.helpers.usability
import operator


class User(pyrekall.models.common.AbstractWrapper):
    def __init__(self, u, v, f):
        super(User, self).__init__()

        self.key = str(u.Path)

        self.name = str(v.UserName.Value)
        self.full_name = str(v.FullName.Value)
        self.type = str(v.Type)
        self.comment = str(v.Comment.Value)

        self.account_expiration = f.AccountExpiration
        self.password_failed_time = f.PasswordFailedTime
        self.password_reset_date = f.PwdResetDate
        self.last_login_time = f.LastLoginTime

        self.login_count = int(f.LoginCount)
        self.failed_login_count = int(f.FailedLoginCount)

        self.flags = self.__reverse_user_account_flags_from_maskmap(flags=f.Flags)
        self.rid = int(f.Rid)

        [setattr(self, k, self.unwrap(k, v)) for k, v in self]

    def __reverse_user_account_flags_from_maskmap(self, flags):
        result = []
        c = flags.v()
        for k, v in sorted(flags.maskmap.items(), key=operator.itemgetter(1), reverse=True):
            if v <= c:
                c %= v
                result.append(k)
        return result