# coding: utf-8
import enum

from sqlalchemy import Column, Date, DateTime, Integer, SmallInteger, Text, UniqueConstraint, text, DECIMAL, Numeric, \
    ForeignKey, func, String, Enum
from sqlalchemy.dialects.postgresql import TIMESTAMP, ARRAY
from db.async_database import Base, async_engine
from db.sync_database import sync_engine
import nanoid

metadata = Base.metadata

class UserStatus(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'comment': '用户信息表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment='用户ID')
    nano_id = Column(String, unique=True, index=True, default=nanoid.generate, comment="唯一nanoid")
    username = Column(String(50), unique=False, nullable=True, comment='用户名')
    email = Column(String(120), unique=True, nullable=True, index=True, comment='电子邮件地址')
    phone_number = Column(String, unique=True, comment='手机号')
    password_hash = Column(String(128), nullable=True, comment='密码哈希')
    # full_name = Column(String(100), comment='全名')
    # is_active = Column(Boolean, default=True, comment='是否活跃')
    # is_admin = Column(Boolean, default=False, comment='是否管理员')
    # 微信相关字段
    wechat_openid = Column(String(128), unique=True, nullable=True, comment='微信OpenID')
    wechat_unionid = Column(String(128), unique=True, nullable=True, comment='微信UnionID')
    wechat_nickname = Column(String(100), comment='微信昵称')
    wechat_avatar_url = Column(Text, comment='微信头像URL')

    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.PENDING)
    create_time = Column(TIMESTAMP(precision=0), server_default=func.now(), comment='创建时间')
    update_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def __repr__(self):
        return (f"id={self.id}, nano_id={self.nano_id}, username={self.username}, "
                f"email={self.email}, wechat_openid={self.wechat_openid}, "
                f"wechat_unionid={self.wechat_unionid}, wechat_nickname={self.wechat_nickname}, "
                f"wechat_avatar_url={self.wechat_avatar_url}, status={self.status}, "
                f"create_time={self.create_time}, update_time={self.update_time}")
    # def __repr__(self):
    #     return f"<User(nano_id='{self.nano_id}', username='{self.username}', email='{self.email}'>"
    def to_dict(self):
        return {
            "id": self.id,
            "nano_id": self.nano_id,
            "username": self.username,
            "email": self.email,
            "wechat_openid": self.wechat_openid,
            "wechat_unionid": self.wechat_unionid,
            "wechat_nickname": self.wechat_nickname,
            "wechat_avatar_url": self.wechat_avatar_url,
            "status": self.status.value,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat()
        }

class GuideInfo(Base):
    __tablename__ = 'guide_info'
    __table_args__ = {'comment': '途钉指南详情'}

    id = Column(Integer, primary_key=True,  autoincrement=True, comment='指南Id')
    userid = Column(Integer, ForeignKey('user.id'), nullable=False, comment='创建该guide的用户ID')
    location_ids = Column(ARRAY(Integer), comment='地点ID列表')
    statue = Column(Integer, server_default=text("1"), comment='订单状态（1:订单就绪，还没支付 2：已支付成功 3：取消订单')
    create_time = Column(TIMESTAMP(precision=0), server_default=func.now(), comment='创建时间')
    update_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment='更新时间')

# 其他相关模型和配置...

if __name__ == '__main__':
    metadata.create_all(sync_engine)