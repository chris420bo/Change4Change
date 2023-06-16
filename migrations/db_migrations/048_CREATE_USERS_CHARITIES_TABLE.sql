CREATE TABLE UsersCharities (
    user_id int,
    Meals bool,
    Red bool,
    Heart bool,
    NYC bool,
    NY bool,

    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)

);