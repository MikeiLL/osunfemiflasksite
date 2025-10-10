-- Table names are flush left, and column definitions are
-- indented by at least one space or tab. Blank lines and
-- lines beginning with a double hyphen are comments.

users
	id serial primary key
	displayname varchar not null unique
  ifaorishaname varchar
	email varchar not null unique
	password varchar not null default ''
	user_level int not null default 1 -- noaccess=0, manager=1, admin=3
  grade_level int not null default 1 -- for access to classes
-- subscription_type Stripe subscriptions

-- TODO users stores reference won't work when running
-- the script because the stores table is not yet created
