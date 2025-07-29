import datetime
import enum
import logging

import ics
import isodate

from holocal.errors import HolocalException

log = logging.getLogger(__name__)


class Event:
    def __init__(self, site, talent, datetime):
        self.site = site
        self.talent = talent
        self.datetime = datetime
        self.show = True
        self.end = None
        self.estimated_end_time = False
        self.duration = None

    def ical_event(self) -> ics.Event:
        kwargs = {}
        if self.end:
            kwargs["end"] = self.end

        elif self.duration:
            kwargs["duration"] = self.duration

        else:
            kwargs["duration"] = {"hours": 2}
            self.estimated_end_time = True

        description = f"{self.title}\n{self.site.url}"
        if self.estimated_end_time:
            description += "\n\n※終了時刻は推定です。\n" \
                "Note: The end time is an estimate."

        return ics.Event(
            name=f"{self.talent}: {self.title}",
            begin=self.datetime,
            description=description,
            # use video_id as uid will make order of events static
            # (because uid is used in Event.__hash__)
            uid=self.site.id,  # TODO: コラボで同じ動画が複数ホロジュールに登録される可能性？
            url=self.site.url,
            **kwargs,
        )

    def assign(self, meta: dict) -> bool:
        end_time = None

        match meta:
            case {"snippet": {"title": title},
                  "liveStreamingDetails": {"actualStartTime": time,
                                           "actualEndTime": end_time}}:
                self.begin = self._parse_datetime(time)
                self.end = self._parse_datetime(end_time)

                # どういうわけか終了時間が開始時間より前にくる場合がありそうなので。
                if self.begin >= self.end:
                    self.end = self.begin + datetime.timedelta(hours=2)
                    self.estimated_end_time = True

            case {"snippet": {"title": title},
                  "liveStreamingDetails": {"scheduledStartTime": time}}:
                self.begin = self._parse_datetime(time)
                self.end = max(self.begin, datetime.datetime.now()) \
                    + datetime.timedelta(hours=2)
                self.estimated_end_time = True

            # "publishedAt" is for video case.
            # TODO: is this correct?
            case {"snippet": {"title": title, "publishedAt": time},
                  "contentDetails": {"duration": duration}}:
                self.begin = self._parse_datetime(time)
                self.duration = isodate.parse_duration(duration)

            case None:
                match self.site.type:
                    case Type.Twitch | Type.Abema:
                        self.title = self.site.type.name
                        return

                    case Type.YouTube:
                        log.warn("Possibly private video?  "
                                 "Empty metadata.  "
                                 f"{repr(self)}")
                        self.show = False
                        return

        if not title or not time:
            raise HolocalException(f"missing value: {repr(meta)}")

        self.title = title

    def _parse_datetime(self, source):
        return datetime.datetime.strptime(source, "%Y-%m-%dT%H:%M:%SZ")

    def __repr__(self):
        return f"<{self.site}\t{self.talent}\t{self.datetime}>"


class Talent:
    def __init__(self, name, mark=None):
        self.name = name
        self.mark = mark

    def __str__(self):
        """This is used in event name (summary)."""
        mark = self.mark or ""
        return f"{mark}{self.name}"

    def __repr__(self):
        if self.mark:
            return f"<{self.name} {self.mark}>"

        else:
            return f"<{self.name}>"


class Type(enum.Enum):
    YouTube = "YouTube"
    Abema = "Abema"
    Twitch = "Twitch"
