from src.main import db


class Move(db.Model):
    __tablename__ = "moves"

    move_id = db.Column(db.Integer, primary_key=True)
    move_name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<(#{self.move_id} {self.move_name})>"
