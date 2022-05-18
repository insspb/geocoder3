# Confidence Score

Confidence score based on [OpenCage API](https://opencagedata.com/api#confidence)
implementation, but available in any supported geocoder. For geocoders without default
confidence score support this property calculated by same definition in `geocoder3`
internal process.

## What is this

The OpenCage Geocoder will always attempt to find a match for as many parts of a query
as it can, but this isn't always possible to do. Where a partial match is made, for
example a street name can be matched but a specific house number on that street cannot
be matched, the geocoder will still return a result but the granularity of the match
will not be as high as if the house number was matched.

The confidence that the geocoder has in a match returned to the confidence field. This
contains a value between 0 and 10, where 0 reflects no confidence and 10 reflects high
confidence.

Confidence is calculated by measuring the distance in kilometres between the South West
and North East corners of each results bounding box; a smaller distance represents a
high confidence while a large distance represents a lower confidence.

The best way to think of our confidence score is as a measure of how confident we
are that centre point coordinates returned for the result precisely reflect the
result. So for example, if you search for "Berlin, Germany", we know exactly where
that is, but it has a confidence of only 4, as Berlin is a large city (and
Bundesland, but that's another story). The coordinates we return are in the centre
of the bounding box, but it would be valid to consider anywhere in that box to be
"Berlin", hence the relatively low confidence score.

|Score |       Description          |
|:----:|:---------------------------|
| 10   | less than 0.25 km distance |
| 9    | less than 0.5 km distance  |
| 8    | less than 1 km distance    |
| 7    | less than 5 km distance    |
| 6    | less than 7.5 km distance  |
| 5    | less than 10 km distance   |
| 4    | less than 15 km distance   |
| 3    | less than 20 km distance   |
| 2    | less than 25 km distance   |
| 1    | 25 km or greater distance  |
| 0    | unable to determine a bounding box|
