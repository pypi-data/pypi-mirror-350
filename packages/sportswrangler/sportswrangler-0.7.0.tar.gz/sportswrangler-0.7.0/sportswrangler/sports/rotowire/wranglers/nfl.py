from sportswrangler.sports.rotowire.wranglers.base import RotoWireWrangler
from sportswrangler.utils.enums import Sport


class RotoWireNFLWrangler(RotoWireWrangler):
    sport: Sport = Sport.NFL

    def get_news(
        self,
        date: str = None,
        hours: int = None,
        max_priority: int = None,
        with_analysis: bool = None,
    ):
        """
        :param date: date to get news from in "YYYY-MM-DD" format
        :param hours: number of hours back from date to get news
        :param max_priority: max priority to get news for, the lower the priority number, the more important it is
        :param with_analysis: flag to determine whether you only want news that has analysis

        Will always return the raw response JSON regardless of the `preferred_dataframe` configuration
        """
        params = {
            "date": date,
            "hours": hours,
            "max_priority": max_priority,
            "with_analysis": (
                1 if with_analysis else 0 if with_analysis is not None else None
            ),
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = self.base_request(api_path="/News.php", additional_params=params)
        return response.json()
