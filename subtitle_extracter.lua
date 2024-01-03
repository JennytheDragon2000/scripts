-- Open the subtitle file in read mode
local file = io.open("/tmp/sub.srt", "r")

if not file then
	print("Could not open file")
	return
end

-- Variables to store your desired timestamps
local startTime = "00:02:00,000" -- adjust this
local endTime = "00:05:00,000" -- adjust this

-- Variable to store the current subtitle block
local currentSubtitle = ""
-- Variable to indicate whether we're within the desired time range
local inTimeRange = false

-- Iterate over each line in the file
for line in file:lines() do
	-- If the line contains a timestamp
	if line:match("%d+:%d+:%d+,%d+ --> %d+:%d+:%d+,%d+") then
		-- Check if the line's timestamp is within the desired range
		local start, stop = line:match("^(%d+:%d+:%d+,%d+) --> (%d+:%d+:%d+,%d+)")
		if start >= startTime and stop <= endTime then
			inTimeRange = true
		else
			inTimeRange = false
		end
	elseif inTimeRange then
		-- If the line is a subtitle and we're within the time range, add it to the current subtitle
		currentSubtitle = currentSubtitle .. line .. "\n"
	end
end

-- Close the file
file:close()

-- Open a new file in write mode
local outFile = io.open("extracted_subtitle.txt", "w")

if not outFile then
	print("Could not open output file")
	return
end
-- Write the extracted subtitle to the new file
outFile:write(currentSubtitle)

-- Close the new file
outFile:close()
