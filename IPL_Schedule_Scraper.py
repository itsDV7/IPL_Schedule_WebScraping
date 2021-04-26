from bs4 import BeautifulSoup
import requests
import arrow
import csv

html_page = requests.get('https://www.iplt20.com/matches/schedule/men').text
soup = BeautifulSoup(html_page, 'lxml')


def ipl_schedule():
    dates = soup.find_all(name='h3', class_='match-list__date js-date')
    match_fixture_data = soup.find_all(name='div', class_='match-list__item')
    with open('IPL_Calendar', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Subject", "Start Date", "Start Time", "Description", "Location"])
        for date in dates:
            search_date = arrow.get(date.text, 'dddd, Do MMMM YYYY').format('YYYY-MM-DD')
            cal_date = arrow.get(date.text, 'dddd, Do MMMM YYYY').format('MM/DD/YYYY')
            fixtures = [match for match in match_fixture_data if search_date in match['data-timestamp']]
            for match in fixtures:
                teams = match.find_all(name='p', class_='fixture__team-name fixture__team-name--abbrv')
                team1 = teams[0].text
                team2 = teams[1].text
                match_time = match.find(class_='fixture__time')
                cal_match_time = arrow.get(match_time.text, 'HH:mm').format('hh:mm A')
                match_number = match.find(class_='fixture__description').text
                match_stadium = match.find(name='span').contents[1].strip()
                writer.writerow(
                    ["{} vs {}".format(team1, team2), cal_date, cal_match_time, match_number, match_stadium])
    print("Calendar Exported!")


def ipl_schedule_team(team):
    match_fixture_data = [match for match in soup.find_all(name='div', class_='match-list__item') if team in match
    ['class'][-1]]
    with open(f'IPL_Calendar_{team}', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Subject", "Start Date", "Start Time", "Description", "Location"])
        for match in match_fixture_data:
            cal_date, cal_match_time = arrow.get(match['data-timestamp'].split('T')[0], 'YYYY-MM-DD').format('MM/DD/YYYY'), arrow.get(match['data-timestamp'].split('T')[1].split('+')[0], 'HH:mm:ss').format('hh:mm A')
            fixture_teams = match.find_all(name='p', class_='fixture__team-name fixture__team-name--abbrv')
            team1 = fixture_teams[0].text
            team2 = fixture_teams[1].text
            fixture_info = match.find(name='div', class_='fixture__info')
            match_number = fixture_info.find(name='span', class_='fixture__description').text
            match_stadium = fixture_info.span.contents[1].strip()
            writer.writerow(["{} vs {}".format(team1, team2), cal_date, cal_match_time, match_number, match_stadium])
    print(f"{team} Calendar Exported")


if __name__ == '__main__':
    print("IPL Schedule Scraper\n")
    print("Teams:\n1. CSK\n2. RCB\n3. DC\n4. MI\n5. PBKS\n6. RR\n7. SRH\n8. KKR\n9. ALL\n")
    print("Select a Team:\n")
    select_team = input("> ")
    if select_team in [' ', '\n', 'all', 'ALL']:
        ipl_schedule()
    elif select_team in ['CSK', 'RCB', 'DC', 'MI', 'PBKS', 'RR', 'SRH', 'KKR', 'Chennai Super Kings',
                         'Royal Challengers Bangalore', 'Delhi Capitals', 'Mumbai Indians', 'Punjab Kings',
                         'Rajasthan Royals', 'Sunrisers Hyderabad', 'Kolkata Knight Riders']:
        ipl_schedule_team(select_team)
    else:
        print(f"Unable to find team {select_team}\n")
        print("Defaulting to ALL teams...\n")
        ipl_schedule()
