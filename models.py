

class Payment(BaseModel):
    id: str
    user_id: str
    property_id: str
    amount: float
    currency: str = "INR"
    status: str  # pending, completed, refunded, failed
    razorpay_order_id: Optional[str]
    razorpay_payment_id: Optional[str]
    stripe_payment_intent_id: Optional[str]
    created_at: datetime
    updated_at: datetime

class Admin(BaseModel):
    id: str
    username: str
    email: str
    password: str  # hashed
    role: str = "admin"  # admin, moderator, superadmin
    permissions: List[str]
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]

class AdminLog(BaseModel):
    admin_id: str
    action: str  # login, logout, user_updated, property_approved, etc.
    target_user_id: Optional[str]
    target_property_id: Optional[str]
    timestamp: datetime
    ip_address: Optional[str]
    