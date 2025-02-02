class ValidationResult(Base):
    """
    Database Model for Email Validation Results
    """
    __tablename__ = 'validation_results'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    syntax_valid = Column(Boolean, default=False)
    domain_exists = Column(Boolean, default=False)
    mx_records_valid = Column(Boolean, default=False)
    mx_record_valid = Column(Boolean, default=False)
    smtp_verified = Column(Boolean, default=False)
    smtp_valid = Column(Boolean, default=False)
    disposable = Column(Boolean, default=False)
    disposable_check = Column(Boolean, default=False)
    role_account = Column(Boolean, default=False)
    typo_detected = Column(Boolean, default=False)
    typo_suggestion = Column(String, nullable=True)
    domain_reputation = Column(Float, default=0.0)
    spam_trap = Column(Boolean, default=False)
    catch_all = Column(Boolean, default=False)
    risk_score = Column(Float, default=0.0, index=True)
    status = Column(String, default="Invalid", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_validation_created_at', 'created_at'),
        Index('idx_validation_status_created', 'status', 'created_at'),
        Index('idx_validation_email_status', 'email', 'status'),
    )