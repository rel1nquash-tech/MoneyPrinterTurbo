from app.trends.library import TopicAngle, TopicSeed, build_topic_library
from app.trends.registry import TrendTopic


_SEEDS = [
    TopicSeed("compound interest", "investing", "Small repeated gains can become powerful when time and reinvestment work together.", ["investing", "basics", "wealth"]),
    TopicSeed("dollar-cost averaging", "investing", "Regular buying can reduce timing stress and build discipline through market swings.", ["investing", "strategy", "beginners"]),
    TopicSeed("index funds", "investing", "Broad market funds offer diversification without needing to pick individual winners.", ["investing", "index funds", "basics"]),
    TopicSeed("dividend investing", "investing", "Dividend strategies focus on cash flow, business quality, and reinvestment decisions.", ["investing", "dividends", "stocks"]),
    TopicSeed("value investing", "investing", "Buying below intrinsic value requires patience, research, and emotional control.", ["investing", "value investing", "stocks"]),
    TopicSeed("growth investing", "investing", "Growth investors look for expanding revenue, markets, and future earnings potential.", ["investing", "growth stocks", "stocks"]),
    TopicSeed("risk tolerance", "investing", "A portfolio only works if the investor can hold it during uncomfortable periods.", ["investing", "risk", "planning"]),
    TopicSeed("asset allocation", "investing", "The mix of stocks, bonds, cash, and alternatives drives much of long-term performance.", ["investing", "portfolio", "risk"]),
    TopicSeed("gold as a store of value", "gold", "Gold is often used as a hedge when confidence in currencies or markets weakens.", ["gold", "inflation", "hedge"]),
    TopicSeed("gold versus stocks", "gold", "Gold and equities behave differently because one stores value while the other produces earnings.", ["gold", "stocks", "investing"]),
    TopicSeed("central banks and gold", "gold", "Central banks hold gold for reserves, trust, and diversification beyond paper currencies.", ["gold", "central banks", "macro"]),
    TopicSeed("gold price drivers", "gold", "Rates, inflation expectations, currency strength, and fear can all move gold prices.", ["gold", "macro", "markets"]),
    TopicSeed("physical gold versus gold ETFs", "gold", "Owning bars, coins, or fund shares creates different costs, risks, and convenience tradeoffs.", ["gold", "etfs", "personal finance"]),
    TopicSeed("inflation basics", "inflation", "Inflation means money buys less over time, changing prices, wages, and savings decisions.", ["inflation", "basics", "macro"]),
    TopicSeed("real returns", "inflation", "Investment gains only matter after subtracting inflation and fees.", ["inflation", "investing", "returns"]),
    TopicSeed("interest rates and inflation", "inflation", "Central banks often raise rates to cool demand and slow price increases.", ["inflation", "rates", "macro"]),
    TopicSeed("wage inflation", "inflation", "Rising wages can help households but also affect business costs and pricing.", ["inflation", "wages", "economy"]),
    TopicSeed("shrinkflation", "inflation", "Companies sometimes keep prices stable while reducing package size or quality.", ["inflation", "consumer", "personal finance"]),
    TopicSeed("ETF basics", "etfs", "ETFs trade like stocks while holding baskets of assets inside one fund.", ["etfs", "investing", "basics"]),
    TopicSeed("expense ratios", "etfs", "Small annual fund fees can create large long-term differences in investor outcomes.", ["etfs", "fees", "investing"]),
    TopicSeed("S&P 500 ETFs", "etfs", "S&P 500 funds give exposure to large U.S. companies through one simple vehicle.", ["etfs", "s&p 500", "stocks"]),
    TopicSeed("bond ETFs", "etfs", "Bond funds can add income and stability but still react to rate changes.", ["etfs", "bonds", "rates"]),
    TopicSeed("sector ETFs", "etfs", "Sector funds concentrate exposure in areas like technology, energy, or healthcare.", ["etfs", "sectors", "stocks"]),
    TopicSeed("emergency funds", "personal-finance", "Cash reserves protect plans when income drops or surprise expenses arrive.", ["personal finance", "saving", "basics"]),
    TopicSeed("budgeting systems", "personal-finance", "A budget turns income into decisions before lifestyle creep spends it automatically.", ["personal finance", "budgeting", "money habits"]),
    TopicSeed("credit scores", "personal-finance", "Payment history, utilization, and account age can affect borrowing costs.", ["personal finance", "credit", "debt"]),
    TopicSeed("good debt versus bad debt", "personal-finance", "Debt can build assets or drain cash flow depending on cost and purpose.", ["personal finance", "debt", "basics"]),
    TopicSeed("lifestyle inflation", "personal-finance", "Earning more does not build wealth if every raise becomes a new fixed expense.", ["personal finance", "saving", "behavior"]),
    TopicSeed("retirement accounts", "personal-finance", "Tax-advantaged accounts can change how quickly long-term savings compound.", ["personal finance", "retirement", "taxes"]),
    TopicSeed("stock market indexes", "stock-market-basics", "Indexes track groups of stocks and provide a snapshot of market performance.", ["stock market", "indexes", "basics"]),
    TopicSeed("bull and bear markets", "stock-market-basics", "Market cycles shape investor psychology and create very different decision environments.", ["stock market", "cycles", "basics"]),
    TopicSeed("market capitalization", "stock-market-basics", "Market cap measures company value by multiplying share price by shares outstanding.", ["stock market", "valuation", "basics"]),
    TopicSeed("price-to-earnings ratios", "stock-market-basics", "The P/E ratio compares a stock price to the earnings behind it.", ["stock market", "valuation", "basics"]),
    TopicSeed("earnings reports", "stock-market-basics", "Quarterly reports reveal revenue, profit, guidance, and management expectations.", ["stock market", "earnings", "stocks"]),
    TopicSeed("stock splits", "stock-market-basics", "A split changes share count and price per share without changing business value.", ["stock market", "stocks", "basics"]),
    TopicSeed("market bubbles", "stock-market-basics", "Bubbles form when prices detach from fundamentals and narratives overpower caution.", ["stock market", "history", "risk"]),
    TopicSeed("rebalancing", "investing", "Rebalancing restores a portfolio's target mix after markets move.", ["investing", "portfolio", "risk"]),
    TopicSeed("tax-loss harvesting", "investing", "Selling losing positions can offset gains when done within tax rules.", ["investing", "taxes", "portfolio"]),
    TopicSeed("behavioral finance", "personal-finance", "Biases like loss aversion and herd behavior often drive costly money decisions.", ["personal finance", "behavior", "investing"]),
    TopicSeed("financial independence", "personal-finance", "Financial independence depends on savings rate, expenses, investments, and time.", ["personal finance", "retirement", "wealth"]),
]

_ANGLES = [
    TopicAngle("{label} explained in 45 seconds", "Most people make this harder than it needs to be.", "Give a clear Shorts explanation of {label}: {detail}", ["explainer", "shorts"]),
    TopicAngle("The mistake beginners make with {label}", "This one mistake can quietly cost years of progress.", "Show the common beginner trap around {label}: {detail}", ["beginners", "mistakes"]),
    TopicAngle("Why {label} matters before you invest", "Understanding this can change how you react to risk.", "Connect {label} to practical investing decisions: {detail}", ["investing", "education"]),
    TopicAngle("{label}: simple example, real lesson", "A quick example makes the concept click.", "Turn {label} into a simple numerical or real-world example: {detail}", ["example", "financial literacy"]),
    TopicAngle("How smart investors think about {label}", "The goal is not prediction; it is better decision making.", "Frame {label} through long-term investor behavior: {detail}", ["strategy", "mindset"]),
]

_VOICES = [
    "calm finance educator",
    "clear market explainer",
    "practical money coach",
    "data-driven narrator",
]

_TOPICS = build_topic_library("finance", _SEEDS, _ANGLES, _VOICES)


def get_daily_topics(limit: int) -> list[TrendTopic]:
    return _TOPICS[: max(limit, 0)]
