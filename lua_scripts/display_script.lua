local displayGroup = workspace.Displays
local display_no = 0	

local displays = {}
for _, display in ipairs(displayGroup:GetChildren()) do
	if string.match(display.Name, "SpotifyDisplay%d+") then
		table.insert(displays, {
			artist_display = display["Artist Display"].SurfaceGui.TextLabel,
			song_display = display["Song Display"].SurfaceGui["Song Title (Editable)"],
			song_no = display["Song Display"].SurfaceGui["Number"]
		})
	end
end

for i, item in ipairs(data) do
	if displays[i] then
		local display = displays[i]
		display.artist_display.Text = "Artist Name: " .. item.artist
		display.song_display.Text = item.song
		display_no = display_no + 1
		display.song_no.Text = "("..display_no..")"
		print("Set display ".. i)
	else
		print("Display "..i.." not found")
	end
end