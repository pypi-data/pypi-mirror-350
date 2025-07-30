from pymediainfo import MediaInfo


def get_media_metadata(filepath):
    media_info = MediaInfo.parse(filepath)
    tracks = {x['track_type']: x for x in (t.to_data() for t in media_info.tracks)}
    general = tracks['General']
    base_info = dict(s=general['file_size'], e=general.get('file_extension'))
    image = tracks.get('Image')
    if image:
        return dict(
            **base_info,
            f=image['format'],
            w=image['width'],
            h=image['height'],
        )
    video = tracks.get('Video')
    if video:
        return dict(
            **base_info,
            f=video['format'],
            d=video['duration'],
            w=video['width'],
            h=video['height'],
        )
    audio = tracks.get('Audio')
    if audio:
        return dict(
            **base_info,
            f=audio['format'],
            d=audio['duration']
        )
    return base_info
