from html import escape
from typing import List, Optional

from tube_search.exceptions import VideoSearchFailed, VideoNotFound
from tube_search.structs import TubeAccessibilityInfo, TubeChannelInfo, TubeThumbnailsInfo, TubeShelfInfo, TubeViewsInfo, TubeVideoInfo
from tube_search.utils import TubeEnums, TubeUtils, YouTubeSearchUtils

class VideoSearch(TubeUtils):
    def _parseVideoComponent(self, element: dict, shelfTitle: str | None) -> TubeVideoInfo:
        """
        Formats video components in attribute format, making it easier to capture information.

        Args:
            element - (dict): VideoRenderer elements, formatted in a dictionary of information.
            shielfTitle - (str | None): Title of the video shelf type.
        
        Returns:
            TubeVideoInfo: Video information formatted in classes, for greater ease in handling information.
        """

        video = element[TubeEnums.VIDEO_ELEMENT.value]
        return TubeVideoInfo(
            videoID=self.getValue(video, ["videoId"]),
            videoTitle=self.getValue(video, ["title", "runs", 0, "text"]),
            videoDuration=self.getValue(video, ["lengthText", "simpleText"]),
            publishedTime=self.getValue(video, ["publishedTimeText", "simpleText"]),
            videoViewCount=TubeViewsInfo(
                view_count=self.getValue(video, ["viewCountText", "simpleText"]),
                view_abbr_count=self.getValue(video, ['shortViewCountText', 'simpleText']),
            ),
            thumbnails=[
                TubeThumbnailsInfo(**photo) for photo in self.getValue(video, ["thumbnail", "thumbnails"])
            ],
            descriptionSnippet=escape("".join(
                run.get("text")
                for snippet in self.getValue(video, ["detailedMetadataSnippets"])
                if snippet.get("snippetText")
                for run in snippet.get("snippetText", {}).get("runs", [])
            )) if self.getValue(video, ["detailedMetadataSnippets"]) else None,
            channel=TubeChannelInfo(
                title=self.getValue(video, ["ownerText", "runs", 0, "text"]),
                id=self.getValue(video, ["ownerText", "runs", 0, "navigationEndpoint", "browseEndpoint", "browseId"]),
                thumbnails=[
                    TubeThumbnailsInfo(**photo) for photo in self.getValue(video, ["channelThumbnailSupportedRenderers", "channelThumbnailWithLinkRenderer", "thumbnail", "thumbnails"])
                ],
                url="https://www.youtube.com/channel/{channelID}".format(channelID=self.getValue(video, ['ownerText', 'runs', 0, 'navigationEndpoint', 'browseEndpoint', 'browseId'])),
            ),
            accessibility=TubeAccessibilityInfo(
                title=self.getValue(video, ["title", "accessibility", "accessibilityData", "label"]),
                duration=self.getValue(video, ["lengthText", "accessibility", "accessibilityData", "label"])
            ),
            url="https://www.youtube.com/watch?v={videoID}".format(videoID=self.getValue(video, ["videoId"])),
            shelfTitle=shelfTitle
        )
    
    async def _getVideoSource(
        self,
        query: str,
        language: str,
        region: str,
        searchPreferences: str,
    ) -> List[dict]:
        """
        Search and separates only the main information from the video.

        Args:
            query - (str): The search term provided by the user. This is the main subject of the search (e.g., 'Elektronomia - NCS').
            language - (str): The language code indicating the desired language for the search results (e.g., 'en-US' for English (USA), 'pt-BR' for Portuguese (Brazil).)
            region - (str): The region code specifying the geographic area for the search results (e.g., 'US' for United States, 'BR' for Brazil).
            searchPreferences - Optional(str): Additional search parameters or preferences, often encoded as a string. This allows for more specific search configurations.

        Returns:
            List[dict]: A formatted list of information containing the main research information.
        """
        r = await YouTubeSearchUtils().search(
            query=query,
            language=language,
            region=region,
            searchPreferences=searchPreferences,
        )
        parsedResponse, _ = YouTubeSearchUtils().parseSourceResponse(
            response=r, 
            continuationKey=None,
        )
        return parsedResponse
    
    async def videos(
        self,
        query: str,
        language: str,
        region: str,
        limit: Optional[int] = 20,
    ) -> List[TubeVideoInfo]:
        """
        Search up to 20 videos at once and get video information, following the user-imposed [limit].

        Args:
            query - (str): The search term provided by the user. This is the main subject of the search (e.g., 'Elektronomia - NCS').
            language - (str): The language code indicating the desired language for the search results (e.g., 'en-US' for English (USA), 'pt-BR' for Portuguese (Brazil).)
            region - (str): The region code specifying the geographic area for the search results (e.g., 'US' for United States, 'BR' for Brazil).
            limit - Optional(int): Maximum limit of videos to be returned, (e.g. 10) 10 videos will be returned in total.
        
        Returns:
            List[TubeVideoInfo]: A list with the data of the video searched, using a simple structure and making the code more readable.
        """

        videoList = []
        shelf = TubeShelfInfo(
            title=None,
        )
        videoSource = await self._getVideoSource(
            query=query,
            language=language,
            region=region,
            searchPreferences="EgIQAQ%3D%3D",
        )
        for index, dic in enumerate(videoSource):
            if index > limit:
                break

            try:
                if TubeEnums.SHELF_ELEMENT.value in dic.keys():
                    shelf = YouTubeSearchUtils().getShelfComponent(element=dic)
                if TubeEnums.VIDEO_ELEMENT.value in dic.keys():
                    video = self._parseVideoComponent(dic, shelf.title)
                    videoList.append(video)
                else:
                    continue
            except Exception:
                raise VideoSearchFailed("An unexpected error occurred - Failed to parse video components!")
        
        if len(videoList) == 0:
            raise VideoNotFound("The video you searched for is not available on YouTube.")
        return videoList
    
    async def video(
        self,
        query: str,
        language: str,
        region: str,
    ) -> TubeVideoInfo:
        """
        Search for a video on YouTube and get video informations, based on search parameters.

        Args:
            query - (str): The search term provided by the user. This is the main subject of the search (e.g., 'Elektronomia - NCS').
            language - (str): The language code indicating the desired language for the search results (e.g., 'en-US' for English (USA), 'pt-BR' for Portuguese (Brazil).)
            region - (str): The region code specifying the geographic area for the search results (e.g., 'US' for United States, 'BR' for Brazil).
        
        Returns:
            TubeVideoInfo: Main information about the video searched.
        """

        all_videos = await self.videos(
            query=query,
            language=language,
            region=region,
            limit=1,
        )
        return all_videos.__getitem__(0)