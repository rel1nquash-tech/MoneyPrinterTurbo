from app.trends.library import TopicAngle, TopicSeed, build_topic_library
from app.trends.registry import TrendTopic


_SEEDS = [
    TopicSeed("the 1950 Maracanazo", "world-cup", "Uruguay stunned Brazil in Rio and created one of football's defining World Cup shocks.", ["world cup", "upsets", "brazil", "uruguay"]),
    TopicSeed("Brazil 1970", "world-cup", "Pele, Jairzinho, Tostao, and Carlos Alberto set a lasting standard for attacking football.", ["world cup", "brazil", "pele", "history"]),
    TopicSeed("Argentina 1986", "world-cup", "Diego Maradona shaped a tournament through genius, controversy, and relentless carrying power.", ["world cup", "argentina", "maradona", "history"]),
    TopicSeed("France 1998", "world-cup", "Zinedine Zidane's final headers helped France turn home pressure into a historic first title.", ["world cup", "france", "zidane"]),
    TopicSeed("Spain 2010", "world-cup", "Spain turned possession control into a world title with patience, pressing, and midfield dominance.", ["world cup", "spain", "tactics"]),
    TopicSeed("Germany 2014", "world-cup", "Germany blended structure, depth, and brutal transition play on the way to a fourth star.", ["world cup", "germany", "records"]),
    TopicSeed("Argentina 2022", "world-cup", "Lionel Messi's final World Cup run mixed elite playmaking with emotional momentum.", ["world cup", "argentina", "messi"]),
    TopicSeed("Morocco 2022", "world-cup", "Morocco's compact block and counterattacks powered the first African World Cup semifinal run.", ["world cup", "morocco", "upsets", "tactics"]),
    TopicSeed("Manchester United 1999", "champions-league", "United's stoppage-time comeback against Bayern became the Champions League's ultimate late twist.", ["champions league", "manchester united", "comeback"]),
    TopicSeed("Liverpool 2005", "champions-league", "The Miracle of Istanbul showed how pressure, belief, and tactical changes can flip a final.", ["champions league", "liverpool", "upsets"]),
    TopicSeed("Barcelona 2009", "champions-league", "Pep Guardiola's Barcelona used positional play to control Europe with Messi at the center.", ["champions league", "barcelona", "messi", "tactics"]),
    TopicSeed("Inter Milan 2010", "champions-league", "Jose Mourinho's Inter combined defensive discipline and transition attacks to win the treble.", ["champions league", "inter", "mourinho", "tactics"]),
    TopicSeed("Chelsea 2012", "champions-league", "Chelsea survived wave after wave of pressure to win Europe against Bayern in Munich.", ["champions league", "chelsea", "upsets"]),
    TopicSeed("Real Madrid 2014", "champions-league", "La Decima arrived after years of obsession and one decisive Sergio Ramos header.", ["champions league", "real madrid", "records"]),
    TopicSeed("Real Madrid 2022 comebacks", "champions-league", "Madrid's knockout run turned late goals into a repeatable Champions League weapon.", ["champions league", "real madrid", "comeback"]),
    TopicSeed("Manchester City 2023", "champions-league", "City's treble side used control, pressing, and Erling Haaland's gravity to finally win Europe.", ["champions league", "manchester city", "tactics"]),
    TopicSeed("Pele's global legacy", "famous-players", "Pele became football's first global superstar through World Cups, goals, and cultural reach.", ["pele", "history", "players"]),
    TopicSeed("Diego Maradona's Napoli years", "famous-players", "Maradona lifted Napoli beyond expectations and changed the club's identity forever.", ["maradona", "napoli", "players"]),
    TopicSeed("Lionel Messi's playmaking", "famous-players", "Messi combines dribbling, passing, timing, and finishing in a way few players ever have.", ["messi", "players", "tactics"]),
    TopicSeed("Cristiano Ronaldo's reinvention", "famous-players", "Ronaldo evolved from winger to penalty-box finisher while maintaining elite output.", ["ronaldo", "players", "records"]),
    TopicSeed("Zinedine Zidane's control", "famous-players", "Zidane made high-pressure midfield play look calm through touch, scanning, and balance.", ["zidane", "players", "midfield"]),
    TopicSeed("Ronaldo Nazario's peak", "famous-players", "Ronaldo's acceleration, close control, and finishing made his prime feel almost unfair.", ["ronaldo nazario", "players", "history"]),
    TopicSeed("Marta's influence", "famous-players", "Marta helped raise the standard and visibility of women's football across generations.", ["marta", "players", "women football"]),
    TopicSeed("Kylian Mbappe's speed", "famous-players", "Mbappe turns defensive spacing into panic with timing, acceleration, and direct finishing.", ["mbappe", "players", "tactics"]),
    TopicSeed("total football", "football-history", "Ajax and the Netherlands reshaped how teams think about space, rotation, and pressing.", ["history", "tactics", "ajax"]),
    TopicSeed("the back-pass rule", "football-history", "A single law change forced goalkeepers and defenders to become more technical.", ["history", "rules", "tactics"]),
    TopicSeed("the rise of pressing", "football-history", "Modern pressing turned defending into an attacking weapon by winning the ball higher.", ["history", "pressing", "tactics"]),
    TopicSeed("Bosman ruling", "football-history", "The Bosman ruling changed player power, contracts, and squad building across Europe.", ["history", "transfers", "business"]),
    TopicSeed("women's football growth", "football-history", "Club investment, World Cups, and new stars pushed the women's game into a bigger era.", ["history", "women football", "world cup"]),
    TopicSeed("the libero role", "tactical-analysis", "Sweepers once controlled the game from behind before pressing and back fours changed the job.", ["tactics", "history", "defending"]),
    TopicSeed("false nine systems", "tactical-analysis", "The false nine creates confusion by pulling center backs away from protected spaces.", ["tactics", "false nine", "analysis"]),
    TopicSeed("inverted fullbacks", "tactical-analysis", "Fullbacks moving inside can overload midfield and protect against counterattacks.", ["tactics", "fullbacks", "analysis"]),
    TopicSeed("gegenpressing", "tactical-analysis", "Counter-pressing turns the seconds after losing the ball into a chance to attack again.", ["tactics", "pressing", "analysis"]),
    TopicSeed("low-block defending", "tactical-analysis", "Compact defending can frustrate stronger teams by closing central lanes and forcing crosses.", ["tactics", "defending", "analysis"]),
    TopicSeed("most World Cup goals", "records", "Miroslav Klose's World Cup scoring record rewards timing, movement, and tournament consistency.", ["records", "world cup", "klose"]),
    TopicSeed("Champions League goal records", "records", "Europe's scoring charts reveal longevity, elite service, and repeated knockout impact.", ["records", "champions league", "goals"]),
    TopicSeed("longest unbeaten runs", "records", "Unbeaten streaks show how squad depth and defensive habits survive bad days.", ["records", "history", "consistency"]),
    TopicSeed("fastest goals", "records", "The quickest goals in football usually start with rehearsed pressure and instant execution.", ["records", "goals", "history"]),
    TopicSeed("Greece 2004", "upsets", "Greece used discipline, set pieces, and belief to win one of football's greatest tournament shocks.", ["upsets", "history", "tactics"]),
    TopicSeed("Leicester City 2016", "upsets", "Leicester turned compact defending, speed, and set roles into the Premier League's wildest title.", ["upsets", "premier league", "leicester"]),
]

_ANGLES = [
    TopicAngle("Why {label} still matters", "This story never gets old because it explains football pressure in one minute.", "Break down why {label} remains a strong Shorts topic: {detail}", ["evergreen", "story"]),
    TopicAngle("The hidden tactic behind {label}", "Look past the scoreline and the pattern becomes obvious.", "Explain the tactical idea connected to {label}: {detail}", ["tactical analysis", "shorts"]),
    TopicAngle("What fans forget about {label}", "The famous moment is only half the story.", "Reveal the overlooked context behind {label}: {detail}", ["football history", "context"]),
    TopicAngle("{label}: record, myth, or lesson?", "Some football legends are bigger than the numbers.", "Turn {label} into a fast lesson about records, legacy, and decision making: {detail}", ["records", "analysis"]),
    TopicAngle("How {label} changed football", "One team, player, or match can shift the whole sport.", "Show the lasting influence of {label}: {detail}", ["impact", "history"]),
]

_VOICES = [
    "energetic football analyst",
    "stadium storyteller",
    "calm tactical narrator",
    "documentary sports voice",
]

_TOPICS = build_topic_library("football", _SEEDS, _ANGLES, _VOICES)


def get_daily_topics(limit: int) -> list[TrendTopic]:
    return _TOPICS[: max(limit, 0)]
