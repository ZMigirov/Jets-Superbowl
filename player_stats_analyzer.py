"""
Player Statistics Analyzer Module

This module provides functionality to analyze NFL player statistics,
specifically for the New York Jets and other NFL teams.

Classes:
    Player: Represents an individual player with their statistics.
    PlayerStatsAnalyzer: Analyzes and compares player performance data.

Example:
    >>> analyzer = PlayerStatsAnalyzer()
    >>> analyzer.add_player("Aaron Rodgers", "QB", passing_yards=4694, touchdowns=45)
    >>> stats = analyzer.get_player_stats("Aaron Rodgers")
    >>> print(stats)
"""


class Player:
    """
    Represents an NFL player with their statistics.

    Attributes:
        name (str): Player's full name.
        position (str): Player's position (e.g., QB, RB, WR, DEF).
        stats (dict): Dictionary containing player statistics.
    """

    def __init__(self, name, position, **stats):
        """
        Initialize a Player instance.

        Args:
            name (str): Player's full name.
            position (str): Player's position.
            **stats: Arbitrary keyword arguments representing player statistics.
        """
        self.name = name
        self.position = position
        self.stats = stats

    def __str__(self):
        """Return a formatted string representation of the player."""
        return f"{self.name} ({self.position})"

    def __repr__(self):
        """Return a detailed string representation of the player."""
        return f"Player('{self.name}', '{self.position}', {self.stats})"

    def get_stat(self, stat_name, default=None):
        """
        Get a specific statistic for the player.

        Args:
            stat_name (str): Name of the statistic.
            default: Value to return if statistic doesn't exist.

        Returns:
            The statistic value or default if not found.
        """
        return self.stats.get(stat_name, default)

    def update_stats(self, **new_stats):
        """
        Update player statistics.

        Args:
            **new_stats: Arbitrary keyword arguments to update statistics.
        """
        self.stats.update(new_stats)


class PlayerStatsAnalyzer:
    """
    Analyzes and compares player statistics.

    This class provides methods to manage player data and perform
    statistical analysis and comparisons.
    """

    def __init__(self):
        """Initialize the PlayerStatsAnalyzer with an empty player database."""
        self.players = {}

    def add_player(self, name, position, **stats):
        """
        Add a new player to the analyzer.

        Args:
            name (str): Player's full name.
            position (str): Player's position.
            **stats: Arbitrary keyword arguments representing player statistics.

        Returns:
            Player: The created Player instance.
        """
        player = Player(name, position, **stats)
        self.players[name] = player
        return player

    def remove_player(self, name):
        """
        Remove a player from the analyzer.

        Args:
            name (str): Player's full name.

        Returns:
            bool: True if player was removed, False if not found.
        """
        if name in self.players:
            del self.players[name]
            return True
        return False

    def get_player_stats(self, name):
        """
        Get statistics for a specific player.

        Args:
            name (str): Player's full name.

        Returns:
            dict: Player's statistics or None if player not found.
        """
        if name in self.players:
            player = self.players[name]
            return {
                "name": player.name,
                "position": player.position,
                "stats": player.stats,
            }
        return None

    def get_players_by_position(self, position):
        """
        Get all players with a specific position.

        Args:
            position (str): Player's position.

        Returns:
            list: List of Player objects with the specified position.
        """
        return [
            player
            for player in self.players.values()
            if player.position.upper() == position.upper()
        ]

    def compare_players(self, name1, name2, stat_name):
        """
        Compare a specific statistic between two players.

        Args:
            name1 (str): First player's name.
            name2 (str): Second player's name.
            stat_name (str): Statistic to compare.

        Returns:
            dict: Comparison results or None if players/stat not found.
        """
        if name1 not in self.players or name2 not in self.players:
            return None

        player1 = self.players[name1]
        player2 = self.players[name2]

        stat1 = player1.get_stat(stat_name)
        stat2 = player2.get_stat(stat_name)

        if stat1 is None or stat2 is None:
            return None

        return {
            "player1": {"name": name1, "value": stat1},
            "player2": {"name": name2, "value": stat2},
            "difference": abs(stat1 - stat2),
            "leader": name1 if stat1 > stat2 else name2,
        }

    def get_top_players(self, stat_name, limit=5):
        """
        Get top players by a specific statistic.

        Args:
            stat_name (str): Statistic to sort by.
            limit (int): Maximum number of players to return (default: 5).

        Returns:
            list: List of top players sorted by the specified statistic.
        """
        players_with_stat = [
            (player, player.get_stat(stat_name))
            for player in self.players.values()
            if player.get_stat(stat_name) is not None
        ]

        sorted_players = sorted(
            players_with_stat, key=lambda x: x[1], reverse=True
        )

        return [
            {
                "name": player.name,
                "position": player.position,
                stat_name: value,
            }
            for player, value in sorted_players[:limit]
        ]

    def calculate_average_stat(self, stat_name):
        """
        Calculate the average value of a statistic across all players.

        Args:
            stat_name (str): Statistic to average.

        Returns:
            float: Average value or None if no players have the statistic.
        """
        stats = [
            player.get_stat(stat_name)
            for player in self.players.values()
            if player.get_stat(stat_name) is not None
        ]

        if not stats:
            return None

        return sum(stats) / len(stats)

    def list_all_players(self):
        """
        List all players in the analyzer.

        Returns:
            list: List of all Player objects.
        """
        return list(self.players.values())


if __name__ == "__main__":
    # Example usage
    analyzer = PlayerStatsAnalyzer()

    # Add Jets players
    analyzer.add_player("Aaron Rodgers", "QB", passing_yards=4694, touchdowns=45)
    analyzer.add_player("Breece Hall", "RB", rushing_yards=1200, touchdowns=8)
    analyzer.add_player("Garrett Wilson", "WR", receptions=90, receiving_yards=1260)

    # Display player information
    print("=== Player Statistics ===\n")
    for player in analyzer.list_all_players():
        print(f"{player}")
        print(f"Stats: {player.stats}\n")

    # Get top performers
    print("=== Top Passing Yards ===")
    top_passing = analyzer.get_top_players("passing_yards")
    for player_info in top_passing:
        print(player_info)

    # Compare players
    print("\n=== Player Comparison ===")
    comparison = analyzer.compare_players(
        "Aaron Rodgers", "Garrett Wilson", "touchdowns"
    )
    if comparison:
        print(f"Touchdowns Comparison:")
        print(f"  {comparison['player1']['name']}: {comparison['player1']['value']}")
        print(f"  {comparison['player2']['name']}: {comparison['player2']['value']}")
        print(f"  Leader: {comparison['leader']}")

    # Calculate averages
    print("\n=== Statistics Averages ===")
    avg_touchdowns = analyzer.calculate_average_stat("touchdowns")
    print(f"Average Touchdowns: {avg_touchdowns:.2f}")
