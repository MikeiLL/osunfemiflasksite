-- Table names are flush left, and column definitions are
-- indented by at least one space or tab. Blank lines and
-- lines beginning with a double hyphen are comments.

-- students will have access to all content _up to_ level achieved
grade_levels
  level int primary key
  name varchar not null default '' -- these fields may or may not be necessary
  description varchar not null default '' -- these fields may or may not be necessary

users
  id serial primary key
  fullname varchar not null -- This is also the base of customer name in Stripe
  ifaorishaname varchar -- may be appended to Stripe customer name
  email varchar not null unique  -- This is also the customer name in Stripe
  password varchar not null default ''
  user_level int not null default 1 -- noaccess=0, manager=1, admin=3
  grade_level int references grade_levels default 0 -- for access to classes
  stripe_customer_id varchar not null default ''

-- TODO users stores reference won't work when running
-- the script because the stores table is not yet created
library_content
  id serial primary key
  title varchar not null default 'untitled'
  description varchar not null default ''
  filename varchar not null
  filecontent bytea not null
  active boolean not null default true
  minimum_grade int references grade_levels
