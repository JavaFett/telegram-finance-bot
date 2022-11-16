create table tip(
    id integer primary key,
    body text
);

create table user(
    id integer primary key
);

create table budget(
    id integer primary key,
    monthly_limit integer,
    id_user integer,
    FOREIGN KEY(id_user) REFERENCES user(id)
);

create table category(
    codename varchar(255) primary key,
    name varchar(255),
    is_base_expense boolean,
    aliases text
);

create table expense(
    id integer primary key,
    amount integer,
    created datetime,
    raw_text text,
    id_user integer,
    category_codename integer,
    FOREIGN KEY(id_user) REFERENCES user(id),
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, is_base_expense, aliases)
values
    ("products", "продукты", true, "еда"),
    ("dinner", "обед", true, "столовая, столовка, ланч, бизнес-ланч, бизнес ланч"),
    ("cafe", "кафе", true, "ресторан, рест, рестик, мак, макдональдс, макдак, kfc, кфс, бк, bk, бургер кинг"),
    ("transport", "поездки", true, "такси, метро, автобус, маршрутка, самолет, блабла, бенз"),
    ("phone", "телефон", true, "тел, тф, теле2, мтс, мегафон, билайн, йота, связь"),
    ("internet", "интернет", true, "инет, inet"),
    ("books", "книги", false, "литература, литра, лит-ра"),
    ("subscriptions", "подписки", false, "подписка, подписки, подписон"),
    ("energize", "энергетики", false, "энергос, энергосы, энергетик, энергетики"),
    ("sigarettes", "сигареты", false, "сиги, сигары, сигареты, пар, парилка, калик"),
    ("other", "прочее", false, "");
