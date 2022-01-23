from itertools import chain

import requests
from bs4 import BeautifulSoup


def run_app(load_dynamic_data):
    """Run NBA Pythagorean Wins Example in Python"""

    nba_2022_html = load_dynamic_nba_2022_html() if load_dynamic_data else load_static_nba_2022_html()
    team_data = extract_team_summary_data(nba_2022_html)

    for _, team_dict in team_data.items():
        output_team_summary(team_dict)


def load_dynamic_nba_2022_html():
    """Load NBA 2022 team summary html from Basketball Reference"""

    html_url = 'https://www.basketball-reference.com/leagues/NBA_2022.html'
    result = requests.get(html_url).content

    return result


def load_static_nba_2022_html():
    """Load NBA 2022 team summary html from Basketball Reference"""

    html_url = 'https://raw.githubusercontent.com/kyleaclark/devcultivation-data/main/basketball/nba-team-summary-01-22-2022.html'
    result = requests.get(html_url).content

    return result


def extract_team_summary_data(nba_html):
    soup_instance = BeautifulSoup(nba_html, features='lxml')

    team_records = scrape_team_records(soup_instance)
    team_totals = scrape_team_totals(soup_instance)
    opponent_totals = scrape_opponent_totals(soup_instance)

    team_data = {}
    for team_item in chain(team_records, team_totals, opponent_totals):
        team_name = team_item.get('team_name')
        if team_name in team_data:
            team_data[team_name].update(team_item)
        else:
            team_data[team_name] = team_item

    result = dict(sorted(team_data.items()))

    return result


def scrape_team_records(soup_instance):
    advanced_stats_soup = soup_instance.find(name='table', attrs={'id': 'advanced-team'})

    team_items = []
    for row in advanced_stats_soup.find_all('tr')[2:-1]:
        try:
            team_items.append({
                'team_name': row.find('td', {'data-stat': 'team'}).text,
                'team_wins': row.find('td', {'data-stat': 'wins'}).text,
                'team_losses': row.find('td', {'data-stat': 'losses'}).text
            })
        except AttributeError:
            pass

    return team_items


def scrape_team_totals(soup_instance):
    team_totals_soup = soup_instance.find(name='table', attrs={'id': 'totals-team'})

    team_items = []
    for row in team_totals_soup.find_all('tr')[1:-1]:
        try:
            team_items.append({
                'team_name': row.find('td', {'data-stat': 'team'}).text,
                'points_scored': row.find('td', {'data-stat': 'pts'}).text
            })
        except AttributeError:
            pass

    return team_items


def scrape_opponent_totals(soup_instance):
    opponent_totals_soup = soup_instance.find(name='table', attrs={'id': 'totals-opponent'})

    team_items = []
    for row in opponent_totals_soup.find_all('tr')[1:-1]:
        try:
            team_items.append({
                'team_name': row.find('td', {'data-stat': 'team'}).text,
                'points_allowed': row.find('td', {'data-stat': 'opp_pts'}).text
            })
        except AttributeError:
            pass

    return team_items


def output_team_summary(team_dict):
    """Output team info and stats"""

    # Define exponent variables
    morey_exponent = 13.91
    hollinger_exponent = 15

    # Define team data variables
    tm_name = team_dict['team_name']
    tm_wins = int(team_dict['team_wins'])
    tm_losses = int(team_dict['team_losses'])
    pts_scored = int(team_dict['points_scored'])  # cast text string to integer
    pts_allowed = int(team_dict['points_allowed'])  # cast text string to integer

    # Compute Pythagorean wins data for the Morey and Hollinger formulas
    m_win_percentage, m_expected_record, m_win_diff = compute_pythagorean_wins(
        morey_exponent, tm_wins, tm_losses, pts_scored, pts_allowed)

    h_win_percentage, h_expected_record, h_win_diff = compute_pythagorean_wins(
        hollinger_exponent, tm_wins, tm_losses, pts_scored, pts_allowed)

    # Output summary aligned and formatted for readability
    tm_record = f'{tm_wins}-{tm_losses}'
    output_summary = (
        f'{tm_name:22} {tm_record:7} {pts_scored} vs {pts_allowed}\n'
        f'{"Morey Expected:":22} {m_win_percentage:.2f}%  {m_expected_record:6} {m_win_diff}\n'
        f'{"Hollinger Expected:":22} {h_win_percentage:.2f}%  {h_expected_record:6} {h_win_diff}\n'
    )
    print(output_summary)


def compute_pythagorean_wins(exponent, tm_wins, tm_losses, pts_scored, pts_allowed):
    """Compute Pythagorean wins data & calculations"""

    win_rate = calculate_win_rate(pts_scored, pts_allowed, exponent)
    win_percentage = round((win_rate * 100), 2)

    games_played = tm_wins + tm_losses
    expected_wins = calculate_expected_wins(win_rate, games_played)
    expected_record = f'{expected_wins}-{games_played-expected_wins}'

    win_diff = expected_wins - tm_wins
    win_diff_str = f'+{win_diff}' if win_diff > 0 else str(win_diff)

    return win_percentage, expected_record, win_diff_str


def calculate_win_rate(pts_scored, pts_allowed, exponent):
    """Calculate Pythagorean win rate"""

    pts_scored_var = pts_scored ** exponent
    pts_allowed_var = pts_allowed ** exponent
    result = pts_scored_var / (pts_scored_var + pts_allowed_var)

    return result


def calculate_expected_wins(win_rate, num_games):
    """Calculate current expected wins"""

    expected_wins = win_rate * float(num_games)
    result = int(round(expected_wins, 0))

    return result


if __name__ == '__main__':
    run_app(load_dynamic_data=True)
