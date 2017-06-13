import pyrekall.helpers.usability
import operator


class User(pyrekall.models.common.AbstractWrapper):
    """
    This class is used to represent users
    """
    def __init__(self, u, v, f):
        super(User, self).__init__()

        self.key = u.Path

        self.name = v.UserName.Value
        self.full_name = v.FullName.Value
        self.type = str(v.Type)
        self.comment = v.Comment.Value
        self.nt_hash = v.NTHash
        self.lan_hash = v.LanHash

        self.account_expiration = f.AccountExpiration.as_datetime().isoformat() or None
        self.password_failed_time = f.PasswordFailedTime.as_datetime().isoformat() or None
        self.password_reset_date = f.PwdResetDate.as_datetime().isoformat() or None
        self.last_login_time = f.LastLoginTime.as_datetime().isoformat() or None

        self.login_count = int(f.LoginCount)
        self.failed_login_count = int(f.FailedLoginCount)

        self.flags = self.__reverse_user_account_flags_from_maskmap(flags=f.Flags)
        self.rid = int(f.Rid)

        super(User, self).post_init()

    def __reverse_user_account_flags_from_maskmap(self, flags):
        """
        This function is used to identify the flags associated with a particular process

        :param flags: an integer representing the flags used by a particular process
        :return: a list of human-readable flags associated with a particular process
        """
        result = []
        c = flags.v()
        for k, v in sorted(flags.maskmap.items(), key=operator.itemgetter(1), reverse=True):
            if v <= c:
                c %= v
                result.append(k)
                continue
        return result

    def summary(self):
        return {
            'key': self.key,
            'user_name': self.name,
            'full_name': self.full_name,
            'comment': self.comment,
            'nt_hash': self.nt_hash,
            'lan_hash': self.lan_hash,
            'type': self.type,
            'account_expiration': self.account_expiration,
            'login_count': self.login_count,
            'failed_login_count': self.failed_login_count,
            'flags': self.flags,
            'password_failed_time': self.password_failed_time,
            'last_login_time': self.last_login_time,
            'rid': self.rid,
            'password_reset_date': self.password_reset_date,
        }


