import sys
from datetime import datetime

from tortoise import fields
from tortoise.queryset import QuerySet
from tortoise import Model as BaseModel
from tortoise.signals import pre_save

# noinspection PyUnresolvedReferences
from x_auth.models import (
    Model,
    Username as Username,
    User as TgUser,
    Proxy as Proxy,
    Dc as Dc,
    Fcm as Fcm,
    App as App,
    Session as Session,
    Peer as Peer,
    UpdateState as UpdateState,
    Version as Version,
    Country as BaseCountry,
)
from x_model.models import TsTrait, DatetimeSecField

from xync_schema.enums import (
    ExType,
    AdStatus,
    OrderStatus,
    ExAction,
    ExStatus,
    PersonStatus,
    UserStatus,
    PmType,
    FileType,
    AddrExType,
)


class Country(BaseCountry):
    cur: fields.ForeignKeyRelation["Cur"] = fields.ForeignKeyField("models.Cur", related_name="countries")
    curexs: fields.ManyToManyRelation["Curex"]
    fiats: fields.BackwardFKRelation["Fiat"]


class Cur(Model):
    id = fields.SmallIntField(True)
    ticker: str = fields.CharField(3, unique=True)
    scale: int = fields.SmallIntField(default=0)
    rate: float | None = fields.FloatField(default=0, null=True)

    pms: fields.ManyToManyRelation["Pm"] = fields.ManyToManyField("models.Pm", through="pmcur")
    exs: fields.ManyToManyRelation["Ex"] = fields.ManyToManyField("models.Ex", through="curex")
    pairs: fields.ReverseRelation["Pair"]
    countries: fields.ReverseRelation[Country]

    _name = {"ticker"}

    class Meta:
        table_description = "Fiat currencies"


class Coin(Model):
    id: int = fields.SmallIntField(True)
    ticker: str = fields.CharField(15, unique=True)
    scale: int = fields.SmallIntField(default=0)
    rate: float | None = fields.FloatField(default=0)
    is_fiat: bool = fields.BooleanField(default=False)
    exs: fields.ManyToManyRelation["Ex"] = fields.ManyToManyField("models.Ex", through="coinex")

    assets: fields.ReverseRelation["Asset"]
    pairs: fields.ReverseRelation["Pair"]
    # deps: fields.ReverseRelation["Dep"]
    # deps_reward: fields.ReverseRelation["Dep"]
    # deps_bonus: fields.ReverseRelation["Dep"]

    _name = {"ticker"}


class Ex(Model):
    id: int = fields.SmallIntField(True)
    name: str = fields.CharField(31)
    host: str | None = fields.CharField(63, null=True, description="With no protocol 'https://'")
    host_p2p: str | None = fields.CharField(63, null=True, description="With no protocol 'https://'")
    url_login: str | None = fields.CharField(63, null=True, description="With no protocol 'https://'")
    type_: ExType = fields.IntEnumField(ExType)
    status: ExStatus = fields.IntEnumField(ExStatus, default=ExStatus.plan)
    logo: str = fields.CharField(511, default="")

    pms: fields.ManyToManyRelation["Pm"]
    curs: fields.ManyToManyRelation[Cur]
    # pmcurs: fields.ManyToManyRelation["Pmcur"] = fields.ManyToManyField("models.Pmcur", through="pmcurex")
    coins: fields.ManyToManyRelation[Coin]

    actors: fields.ReverseRelation["Actor"]
    pmexs: fields.ReverseRelation["Pmex"]
    pairexs: fields.ReverseRelation["PairEx"]
    # deps: fields.ReverseRelation["Dep"]
    tests: fields.ReverseRelation["TestEx"]

    class Meta:
        table_description = "Exchanges"
        unique_together = (("name", "type_"),)

    class PydanticMeta(Model.PydanticMeta):
        include = "name", "logo"

    def client(self, actor: "Actor" = None):
        module_name = f"xync_client.{self.name}.ex"
        __import__(module_name)
        client = sys.modules[module_name].ExClient
        return client(self, actor=actor)


class Curex(BaseModel):
    cur: fields.ForeignKeyRelation[Cur] = fields.ForeignKeyField("models.Cur")
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex")
    exid: str = fields.CharField(32)
    minimum: int = fields.IntField(null=True)
    rounding_scale: int = fields.SmallIntField(null=True)
    countries: fields.ManyToManyRelation[Country] = fields.ManyToManyField(
        "models.Country", through="curexcountry", backward_key="curexs"
    )

    class Meta:
        table_description = "Currency in Exchange"
        unique_together = (("ex_id", "cur_id"), ("ex_id", "exid"))


class Coinex(BaseModel):
    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin")
    coin_id: int
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex")
    minimum: float = fields.FloatField(null=True)

    exid: str = fields.CharField(32)
    p2p: bool = fields.BooleanField(default=True)

    class Meta:
        table_description = "Currency in Exchange"
        unique_together = (("ex_id", "coin_id"), ("ex_id", "exid"))


class Pair(Model):
    id = fields.SmallIntField(True)
    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="pairs")
    cur: fields.ForeignKeyRelation[Cur] = fields.ForeignKeyField("models.Cur", related_name="pairs")

    _name = {"coin__ticker", "cur__ticker"}

    class Meta:
        table_description = "Coin/Currency pairs"
        unique_together = (("coin_id", "cur_id"),)


class PairEx(Model, TsTrait):
    pair: fields.ForeignKeyRelation[Pair] = fields.ForeignKeyField("models.Pair", related_name="pairexs")
    pair_id: int
    fee: float = fields.FloatField(default=0)
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="pairs")
    ex_id: int
    directions: fields.ReverseRelation["Direction"]

    _name = {"pair__coin__ticker", "pair__cur__ticker", "ex__name"}

    class Meta:
        table_description = "Pairs on Exs"
        unique_together = (("pair_id", "ex_id"),)


class Direction(Model):
    id = fields.SmallIntField(True)
    pairex: fields.ForeignKeyRelation[PairEx] = fields.ForeignKeyField("models.PairEx", related_name="directions")
    pairex_id: int
    sell: bool = fields.BooleanField()
    total: int = fields.IntField(null=True)
    ads: fields.ReverseRelation["Ad"]

    _name = {"pairex__coin__ticker", "pairex__cur__ticker", "sell"}

    class Meta:
        table_description = "Trade directions"
        unique_together = (("pairex_id", "sell"),)


class Person(Model, TsTrait):
    status: PersonStatus = fields.IntEnumField(PersonStatus, default=PersonStatus.DEFAULT)
    name: str | None = fields.CharField(127, null=True)

    user: fields.BackwardOneToOneRelation["User"]
    creds: fields.BackwardFKRelation["Cred"]
    actors: fields.BackwardFKRelation["Actor"]
    pm_agents: fields.BackwardFKRelation["PmAgent"]


class User(TgUser, TsTrait):
    status: UserStatus = fields.IntEnumField(UserStatus, default=UserStatus.SLEEP)
    person: fields.OneToOneRelation[Person] = fields.OneToOneField("models.Person", related_name="user")
    person_id: int
    ref: fields.ForeignKeyNullableRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="proteges", null=True
    )
    ref_id: int | None
    contacted_with: fields.ForeignKeyNullableRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="contacts", null=True
    )  # who can texts this user
    contacted_with_id: int | None

    actors: fields.BackwardFKRelation["Actor"]
    contacts: fields.BackwardFKRelation["User"]
    created_forums: fields.BackwardFKRelation["Forum"]
    creds: fields.BackwardFKRelation["Cred"]
    # fiats: fields.BackwardFKRelation["Fiat"]
    gmail: fields.BackwardOneToOneRelation["Gmail"]
    forum: fields.BackwardOneToOneRelation["Forum"]
    limits: fields.BackwardFKRelation["Limit"]
    msgs: fields.BackwardFKRelation["Msg"]
    proteges: fields.BackwardFKRelation["User"]

    # vpn: fields.BackwardOneToOneRelation["Vpn"]
    # invite_requests: fields.BackwardFKRelation["Invite"]
    # invite_approvals: fields.BackwardFKRelation["Invite"]
    # lends: fields.BackwardFKRelation["Credit"]
    # borrows: fields.BackwardFKRelation["Credit"]
    # investments: fields.BackwardFKRelation["Investment"]

    async def free_assets(self):
        assets = await Asset.filter(agent__actor__person__user__id=self.id).values("free", "addr__coin__rate")
        return sum(asset["free"] * asset["addr__coin__rate"] for asset in assets)

    async def fiats_sum(self):
        fiats = await Fiat.filter(cred__person__user__id=self.id).values("amount", "cred__pmcur__cur__rate")
        return sum(fiat["amount"] * fiat["cred__pmcur__cur__rate"] for fiat in fiats)

    async def balance(self) -> float:
        return await self.free_assets() + await self.fiats_sum()

    def name(self):
        return f"{self.first_name} {self.last_name}".rstrip()

    class PydanticMeta(Model.PydanticMeta):
        max_recursion = 0
        include = "role", "status"
        # computed = ["balance"]


@pre_save(User)
async def person(_meta, user: User, _db, _updated: dict) -> None:
    if user.person_id:
        return
    user.person = await Person.create(name=f"{user.first_name} {user.last_name}".strip())


class Gmail(Model):
    login: str = fields.CharField(127)
    password: str = fields.CharField(127)
    auth: dict = fields.JSONField(default={})
    updated_at: datetime | None = DatetimeSecField(auto_now=True)

    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User", "gmail")


class Forum(Model, TsTrait):
    id: int = fields.BigIntField(True)
    joined: bool = fields.BooleanField(default=False)
    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User", "forum")
    user_id: int
    # created_by: fields.BackwardFKRelation[User] = fields.ForeignKeyField("models.User", "created_forums")


class Actor(Model):
    exid: int = fields.BigIntField()
    name: int = fields.CharField(63)
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="actors")
    ex_id: int
    person: fields.ForeignKeyRelation[Person] = fields.ForeignKeyField("models.Person", related_name="actors")
    person_id: int

    agent: fields.BackwardOneToOneRelation["Agent"]
    my_ads: fields.BackwardFKRelation["Ad"]
    taken_orders: fields.BackwardFKRelation["Order"]

    def client(self):
        module_name = f"xync_client.{self.ex.name}.agent"
        __import__(module_name)
        client = sys.modules[module_name].AgentClient
        return client(self, headers=self.agent.auth.get("headers"), cookies=self.agent.auth.get("cookies"))

    def in_client(self):
        module_name = f"xync_client.{self.ex.name}.InAgent"
        __import__(module_name)
        client = sys.modules[module_name].InAgentClient
        return client(self)

    def asset_client(self):
        module_name = f"xync_client.{self.ex.name}.asset"
        __import__(module_name)
        client = sys.modules[module_name].AssetClient
        return client(self)

    class Meta:
        table_description = "Actors"
        unique_together = (("ex_id", "exid"), ("ex_id", "person_id"))


class Agent(Model, TsTrait):
    auth: dict = fields.JSONField(default={})
    actor: fields.OneToOneRelation[Actor] = fields.OneToOneField("models.Actor", "agent")
    actor_id: int

    assets: fields.ReverseRelation["Asset"]

    _name = {"actor__name"}

    # def balance(self) -> int:
    #     return sum(asset.free * (asset.coin.rate or 0) for asset in self.assets)

    # class PydanticMeta(Model.PydanticMeta):
    # max_recursion = 3
    # include = "id", "actor__ex", "auth", "updated_at"
    # computed = ["balance"]


# class Adpm(Model):
#     ad: fields.ForeignKeyRelation["Ad"] = fields.ForeignKeyField("models.Ad")
#     pm: fields.ForeignKeyRelation["Pm"] = fields.ForeignKeyField("models.Pm")
#
#     _name = {"ad__id", "pm__name"}
#
#     class Meta:
#         table_description = "P2P Advertisements - Payment methods"


# class AdCred(Model):
#     ad: fields.ForeignKeyRelation["Ad"] = fields.ForeignKeyField("models.Ad")
#     cred: fields.ForeignKeyRelation["Cred"] = fields.ForeignKeyField("models.Cred")
#
#     _name = {"ad__id", "cred__id"}
#
#     class Meta:
#         table_description = "P2P Advertisements - Payment details"


class Ad(Model, TsTrait):
    exid: int = fields.BigIntField()
    direction: fields.ForeignKeyRelation[Direction] = fields.ForeignKeyField("models.Direction", related_name="ads")
    price: float = fields.FloatField()
    amount: float = fields.FloatField()
    min_fiat: float = fields.FloatField()
    max_fiat: float | None = fields.FloatField(null=True)
    detail: str | None = fields.CharField(4095, null=True)
    auto_msg: str | None = fields.CharField(255, null=True)
    status: AdStatus = fields.IntEnumField(AdStatus, default=AdStatus.active)

    maker: fields.ForeignKeyRelation[Actor] = fields.ForeignKeyField("models.Actor", "my_ads")
    maker_id: int
    pay_req: fields.ForeignKeyNullableRelation["PayReq"] = fields.ForeignKeyField("models.PayReq", "ads", null=True)

    pmexs: fields.ManyToManyRelation["Pmex"] = fields.ManyToManyField("models.Pmex", "adpmex", related_name="ads")
    credexs: fields.ManyToManyRelation["CredEx"] = fields.ManyToManyField(
        "models.CredEx", through="adcredex", related_name="ads"
    )
    orders: fields.ReverseRelation["Order"]

    _icon = "ad"
    _name = {"direction__pairex__coin__ticker", "direction__pairex__cur__ticker", "direction__sell", "price"}

    class Meta:
        table_description = "P2P Advertisements"

    # def epyds(self) -> tuple[PydModel, PydModel, PydModel, PydModel, PydModel, PydModel]:
    #     module_name = f"xync_client.{self.maker.ex.name}.pyd"
    #     __import__(module_name)
    #     return (
    #         sys.modules[module_name].AdEpyd,
    #         sys.modules[module_name].AdFullEpyd,
    #         sys.modules[module_name].MyAdEpydPurchase,
    #         sys.modules[module_name].MyAdInEpydPurchase,
    #         sys.modules[module_name].MyAdEpydSale,
    #         sys.modules[module_name].MyAdInEpydSale,
    #     )


class Pm(Model):
    # name: str = fields.CharField(63)  # mv to pmex cause it diffs on each ex
    norm: str | None = fields.CharField(63)
    acronym: str | None = fields.CharField(7, null=True)
    country: fields.ForeignKeyNullableRelation[Country] = fields.ForeignKeyField("models.Country", "pms", null=True)
    df_cur: fields.ForeignKeyNullableRelation[Cur] = fields.ForeignKeyField("models.Cur", "df_pms", null=True)
    alias: str | None = fields.CharField(63, null=True)
    extra: str | None = fields.CharField(63, null=True)
    ok: bool = fields.BooleanField(default=True)
    bank: bool | None = fields.BooleanField(null=True)

    typ: PmType | None = fields.IntEnumField(PmType, null=True)

    curs: fields.ManyToManyRelation[Cur]
    exs: fields.ManyToManyRelation[Ex] = fields.ManyToManyField("models.Ex", "pmex")  # no need. use pmexs[.exid]
    orders: fields.ReverseRelation["Order"]
    pmcurs: fields.ReverseRelation["Pmcur"]  # no need. use curs
    pmexs: fields.ReverseRelation["Pmex"]

    class Meta:
        table_description = "Payment methods"
        unique_together = (("norm", "country_id"), ("alias", "country_id"))

    # class PydanticMeta(Model.PydanticMeta):
    #     max_recursion = 3
    #     backward_relations = True
    #     include = "id", "name", "logo", "pmexs__sbp"

    # def epyd(self):
    #     module_name = f"xync_client.{self.ex.name}.pyd"
    #     __import__(module_name)
    #     return sys.modules[module_name].PmEpyd


class PmAgent(Model):
    pm: fields.ForeignKeyRelation[Pm] = fields.ForeignKeyField("models.Pm", related_name="agents")
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="pm_agents")
    user_id: int
    auth: dict = fields.JSONField(default={})

    class Meta:
        unique_together = (("pm_id", "user_id"),)


class Pmcur(Model):  # for fiat with no exs tie
    pm: fields.ForeignKeyRelation[Pm] = fields.ForeignKeyField("models.Pm")
    pm_id: int
    cur: fields.ForeignKeyRelation[Cur] = fields.ForeignKeyField("models.Cur")
    cur_id: int

    creds: fields.BackwardFKRelation["Cred"]
    exs: fields.ManyToManyRelation[Ex]

    class Meta:
        table_description = "Payment methods - Currencies"
        unique_together = (("pm_id", "cur_id"),)

    class PydanticMeta(Model.PydanticMeta):
        max_recursion: int = 2  # default: 3
        include = "cur_id", "pm"


class Pmex(BaseModel):  # existence pm in ex with no cur tie
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", "pmexs")
    ex_id: int
    pm: fields.ForeignKeyRelation[Pm] = fields.ForeignKeyField("models.Pm", "pmexs")
    pm_id: int
    logo: fields.ForeignKeyNullableRelation["File"] = fields.ForeignKeyField("models.File", "pmex_logos", null=True)
    logo_id: int
    exid: str = fields.CharField(63)
    name: str = fields.CharField(63)

    ads: fields.ManyToManyRelation[Ad]
    banks: fields.BackwardFKRelation["PmexBank"]

    class Meta:
        unique_together = (("ex_id", "exid"),)  # , ("ex", "pm"), ("ex", "name")  # todo: tmp removed for HTX duplicates


class PmexBank(BaseModel):  # banks for SBP
    pmex: fields.ForeignKeyRelation[Pmex] = fields.ForeignKeyField("models.Pmex", "banks")
    pmex_id: int
    exid: str = fields.CharField(63)
    name: str = fields.CharField(63)

    creds: fields.ManyToManyRelation["Cred"]

    class Meta:
        unique_together = (("pmex", "exid"),)


# class Pmcurex(BaseModel):  # existence pm in ex for exact cur, with "blocked" flag
#     pmcur: fields.ForeignKeyRelation[Pmcur] = fields.ForeignKeyField("models.Pmcur")
#     pmcur_id: int
#     ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex")
#     ex_id: int
#     blocked: bool = fields.BooleanField(default=False)  # todo: move to cureex or pmex?
#
#     # class Meta:
#     #     unique_together = (("ex_id", "pmcur_id"),)


class Cred(Model):
    pmcur: fields.ForeignKeyRelation[Pmcur] = fields.ForeignKeyField("models.Pmcur")
    pmcur_id: int
    detail: str = fields.CharField(84)
    name: str | None = fields.CharField(84, null=True)
    extra: str | None = fields.CharField(84, null=True)
    person: fields.ForeignKeyRelation[Person] = fields.ForeignKeyField("models.Person", "creds")
    person_id: int

    banks: fields.ManyToManyRelation[PmexBank] = fields.ManyToManyField("models.PmexBank", related_name="creds")

    fiat: fields.BackwardOneToOneRelation["Fiat"]
    credexs: fields.BackwardFKRelation["CredEx"]
    orders: fields.BackwardFKRelation["Order"]
    pay_reqs: fields.BackwardFKRelation["PayReq"]

    _name = {"detail"}

    class Meta:
        table_description = "Currency accounts"
        unique_together = (("person_id", "pmcur_id", "detail"),)


class CredEx(Model):
    exid: int = fields.BigIntField()
    cred: fields.ForeignKeyRelation[Cred] = fields.ForeignKeyField("models.Cred", "credexs")
    cred_id: int
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", "credexs")
    ex_id: int

    ads: fields.ManyToManyRelation[Ad]

    _name = {"exid"}

    class Meta:
        table_description = "Credential on Exchange"
        unique_together = (("ex_id", "exid"),)


class Fiat(Model):
    cred: fields.OneToOneRelation[Cred] = fields.OneToOneField("models.Cred", "fiat")
    cred_id: int
    amount: float = fields.FloatField(default=0)
    target: float = fields.FloatField(default=0)
    min_deposit: int = fields.IntField(null=True)

    class Meta:
        table_description = "Currency balances"

    class PydanticMeta(Model.PydanticMeta):
        # max_recursion: int = 2
        backward_relations = False
        include = "id", "cred__pmcur", "cred__detail", "cred__name", "amount"

    @staticmethod
    def epyd(ex: Ex):
        module_name = f"xync_client.{ex.name}.pyd"
        __import__(module_name)
        return sys.modules[module_name].FiatEpyd


class Rival(Model, TsTrait):
    actor: fields.ForeignKeyRelation[Actor] = fields.ForeignKeyField("models.Actor")
    actor_id: int
    direction: fields.ForeignKeyRelation[Direction] = fields.ForeignKeyField("models.Direction")
    direction_id: int
    pm: fields.ForeignKeyRelation[Pm] = fields.ForeignKeyField("models.Pm")
    pm_id: int
    rplace: int = fields.SmallIntField()
    price: float = fields.SmallIntField()
    exec_rate: int = fields.SmallIntField()
    completed: int = fields.SmallIntField()


class Limit(Model):
    pmcur: fields.ForeignKeyRelation[Pmcur] = fields.ForeignKeyField("models.Pmcur")
    pmcur_id: int
    amount: int = fields.IntField(null=True)  # '$' if unit >= 0 else 'transactions count'
    unit: int = fields.IntField(default=30)  # positive: $/days, 0: $/transaction, negative: transactions count / days
    level: float | None = fields.IntField(
        default=0, null=True
    )  # 0 - same group, 1 - to parent group, 2 - to grandparent  # only for output trans, on input = None
    income: bool = fields.BooleanField(default=False)
    added_by: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField("models.User", related_name="limits")
    added_by_id: int

    _name = {"pmcur__pm__name", "pmcur__cur__ticker", "unit", "income", "amount"}

    class Meta:
        table_description = "Currency accounts balance"


class Addr(Model):
    coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="addrs")
    coin_id: int
    actor: fields.ForeignKeyRelation[Actor] = fields.ForeignKeyField("models.Actor", "addrs")
    actor_id: int
    val: str = fields.CharField(127)

    pay_reqs: fields.BackwardFKRelation["PayReq"]

    _name = {"coin__ticker", "free"}

    class Meta:
        table_description = "Coin address on cex"
        unique_together = (("coin_id", "actor_id"),)


class Asset(Model):
    addr: fields.ForeignKeyRelation[Addr] = fields.ForeignKeyField("models.Addr", related_name="addrs")
    addr_id: int
    agent: fields.ForeignKeyRelation[Agent] = fields.ForeignKeyField("models.Agent", "assets")
    agent_id: int

    typ: AddrExType = fields.IntEnumField(AddrExType, default=AddrExType.found)
    free: float = fields.FloatField()
    freeze: float | None = fields.FloatField(default=0)
    lock: float | None = fields.FloatField(default=0)
    target: float | None = fields.FloatField(default=0, null=True)

    _name = {"asset__coin__ticker", "free"}

    class Meta:
        table_description = "Coin balance"
        unique_together = (("addr_id", "agent_id", "typ"),)

    def epyd(self):
        module_name = f"xync_client.{self.agent.ex.name}.pyd"
        __import__(module_name)
        return sys.modules[module_name].AssetEpyd


class PayReq(Model, TsTrait):
    pay_until: datetime = DatetimeSecField()
    addr: fields.ForeignKeyNullableRelation[Addr] = fields.ForeignKeyField("models.Addr", "pay_reqs", null=True)
    addr_id: int
    cred: fields.ForeignKeyNullableRelation[Cred] = fields.ForeignKeyField("models.Cred", "pay_reqs", null=True)
    cred_id: int
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", "pay_reqs")
    user_id: int
    amount: float = fields.FloatField()
    parts: int = fields.IntField(default=1)
    payed_at: datetime | None = DatetimeSecField(null=True)

    ads: fields.ReverseRelation["Ad"]

    _icon = "pay"
    _name = {"ad_id"}

    class Meta:
        table_description = "Payment request"
        unique_together = (("user_id", "cred_id", "addr_id"),)


class Order(Model):
    exid: int = fields.BigIntField()
    ad: fields.ForeignKeyRelation[Ad] = fields.ForeignKeyField("models.Ad", related_name="ads")
    ad_id: int
    amount: float = fields.FloatField()
    cred: fields.ForeignKeyRelation[Cred] = fields.ForeignKeyField("models.Cred", related_name="orders", null=True)
    cred_id: int | None
    taker: fields.ForeignKeyRelation[Actor] = fields.ForeignKeyField("models.Actor", "taken_orders")
    taker_id: int
    maker_topic: int = fields.IntField(null=True)  # todo: remove nullability
    taker_topic: int = fields.IntField(null=True)
    status: OrderStatus = fields.IntEnumField(OrderStatus)
    created_at: datetime | None = DatetimeSecField(auto_now_add=True)
    payed_at: datetime | None = DatetimeSecField(null=True)
    confirmed_at: datetime | None = DatetimeSecField(null=True)
    appealed_at: datetime | None = DatetimeSecField(null=True)

    msgs: fields.BackwardFKRelation["Msg"]

    _name = {"cred__pmcur__pm__name"}

    async def client(self):
        if isinstance(self.ad, QuerySet):
            # noinspection PyTypeChecker
            self.ad: Ad = await self.ad.prefetch_related("agent__ex")
        elif isinstance(self.ad, Ad) and isinstance(self.ad.agent, QuerySet):
            # noinspection PyTypeChecker
            self.ad.agent = await self.ad.agent.prefetch_related("ex")
        elif isinstance(self.ad.agent, Agent) and isinstance(self.ad.agent.ex, QuerySet):
            # noinspection PyTypeChecker
            self.ad.agent.ex = await self.ad.agent.ex
        client = sys.modules[f"xync_client.{self.ad.maker.ex.name}.order"].Client
        return client(self)

    # def epyd(self):  # todo: for who?
    #     module_name = f"xync_client.{self.ex.name}.pyd"
    #     __import__(module_name)
    #     return sys.modules[module_name].OrderEpyd

    class Meta:
        table_description = "P2P Orders"

    class PydanticMeta(Model.PydanticMeta):
        max_recursion: int = 0
        exclude_raw_fields: bool = False
        exclude = ("taker", "ad", "cred", "msgs")


class Msg(Model):
    tgid: int = fields.IntField()
    txt: str = fields.CharField(255)
    read: bool = fields.BooleanField(default=False)
    media: str | None = fields.CharField(255, null=True)
    receiver: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="msgs")
    order: fields.ForeignKeyRelation[Order] = fields.ForeignKeyField("models.Order", related_name="msgs")

    class PydanticMeta(Model.PydanticMeta):
        max_recursion: int = 0
        exclude_raw_fields: bool = False
        exclude = ("receiver", "order")


# class Dep(Model, TsTrait):
#     pid: str = fields.CharField(31)  # product_id
#     apr: float = fields.FloatField()
#     fee: float | None = fields.FloatField(null=True)
#     apr_is_fixed: bool = fields.BooleanField(default=False)
#     duration: int | None = fields.SmallIntField(null=True)
#     early_redeem: bool | None = fields.BooleanField(null=True)
#     type_: DepType = fields.IntEnumField(DepType)
#     # mb: renewable?
#     min_limit: float = fields.FloatField()
#     max_limit: float | None = fields.FloatField(null=True)
#     is_active: bool = fields.BooleanField(default=True)
#
#     coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField("models.Coin", related_name="deps")
#     coin_id: int
#     reward_coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField(
#         "models.Coin", related_name="deps_reward", null=True
#     )
#     reward_coin_id: int | None = None
#     bonus_coin: fields.ForeignKeyRelation[Coin] = fields.ForeignKeyField(
#         "models.Coin", related_name="deps_bonus", null=True
#     )
#     bonus_coin_id: int | None = None
#     ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="deps")
#     ex_id: int
#     investments: fields.ReverseRelation["Investment"]
#
#     _icon = "seeding"
#     _name = {"pid"}
#
#     def repr(self, *args):
#         return f'{self.coin.ticker}:{self.apr * 100:.3g}% {f"{self.duration}d" if self.duration and self.duration > 0 else "flex"}'
#
#     class Meta:
#         table_description = "Investment products"
#         unique_together = (("pid", "type_", "ex_id"),)


# class Investment(Model, TsTrait):
#     dep: fields.ForeignKeyRelation[Dep] = fields.ForeignKeyField("models.Dep", related_name="investments")
#     # dep_id: int
#     amount: float = fields.FloatField()
#     is_active: bool = fields.BooleanField(default=True)
#     user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="investments")
#
#     _icon = "trending-up"
#     _name = {"dep__pid", "amount"}
#
#     def repr(self, *args):
#         return f"{self.amount:.3g} {self.dep.repr()}"
#
#     class Meta:
#         table_description = "Investments"


class TestEx(Model):
    ex: fields.ForeignKeyRelation[Ex] = fields.ForeignKeyField("models.Ex", related_name="tests")
    ex_id: int
    action: ExAction = fields.IntEnumField(ExAction)
    ok: bool | None = fields.BooleanField(default=False, null=True)
    updated_at: datetime | None = DatetimeSecField(auto_now=True)

    _icon = "test-pipe"
    _name = {"ex_id", "action", "ok"}

    def repr(self):
        return f"{self.ex_id} {self.action.name} {self.ok}"

    class Meta:
        table_description = "Test Exs"
        unique_together = (("action", "ex_id"),)

    class PydanticMeta(Model.PydanticMeta):
        max_recursion: int = 2


class Vpn(Model):
    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User", related_name="vpn")
    user_id: int
    priv: str = fields.CharField(63, unique=True)
    pub: str = fields.CharField(63, unique=True)
    created_at: datetime | None = DatetimeSecField(auto_now_add=True)

    _icon = "vpn"
    _name = {"pub"}

    def repr(self):
        return self.user.username

    class Meta:
        table_description = "VPNs"


class File(Model):
    name: str = fields.CharField(178, null=True)
    typ: FileType = fields.IntEnumField(FileType, null=True)
    fid: str = fields.CharField(76, unique=True, null=True)
    ref: bytes = fields.BinaryField(null=True)
    size: bytes = fields.IntField()
    created_at: datetime | None = DatetimeSecField(auto_now_add=True)

    pmex_logos: fields.BackwardFKRelation[Pmex]

    _icon = "file"
    _name = {"name"}

    class Meta:
        table_description = "Files"


# class Invite(Model, TsTrait):
#     ref: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="invite_approvals")
#     ref_id: int
#     protege: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="invite_requests")
#     protege_id: int
#     approved: str = fields.BooleanField(default=False)  # status
#
#     _icon = "invite"
#     _name = {"ref__username", "protege__username", "approved"}
#
#     def repr(self, *args):
#         return self.protege.name
#
#     class Meta:
#         table_description = "Invites"


# class Credit(Model, TsTrait):
#     lender: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="lends")
#     lender_id: int
#     borrower: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="borrows")
#     borrower_id: int
#     borrower_priority: bool = fields.BooleanField(default=True)
#     amount: int = fields.IntField(default=None)  # 0 - is all remain borrower balance
#
#     _icon = "credit"
#     _name = {"lender__username", "borrower__username", "amount"}
#
#     def repr(self, *args):
#         return self.borrower.name
#
#     class Meta:
#         table_description = "Credits"
