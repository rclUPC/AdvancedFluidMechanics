/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Copyright (C) YEAR OpenFOAM Foundation
     \\/     M anipulation  |
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

Description
    Template for use with codeStream.

\*---------------------------------------------------------------------------*/

#include "dictionary.H"
#include "fieldTypes.H"
#include "Ostream.H"
#include "Pstream.H"
#include "read.H"
#include "unitConversion.H"

//{{{ begin codeInclude
#line 45 "/home/robert/GDriveUPC/Documents/asignaturas/AdvancedFluidMechanics/JupyterNotebooks/3-Turbulence/OF11/rotor2D/system/blockMeshDict/#codeStream"
#include "pointField.H"
        #include "SubField.H"
        #include "transformField.H"
//}}} end codeInclude

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

extern "C"
{
    void codeStream_07fd8fb71e70597441cb0476ad0d2368a76d2c1a
    (
        Ostream& os,
        const dictionary& dict
    )
    {
//{{{ begin code
        #line 52 "/home/robert/GDriveUPC/Documents/asignaturas/AdvancedFluidMechanics/JupyterNotebooks/3-Turbulence/OF11/rotor2D/system/blockMeshDict/#codeStream"
// Get the radii. Note using dict.lookupScoped<scalar>("rHub", true, false) instead of dict.lookupScoped<scalar>("rHub", true, false) means that
        // rHub can change without needing to recompile this code. The same is
        // true for access of other settings throughout this file.
        const scalarField rs
        ({
            dict.lookupScoped<scalar>("rHub", true, false),
            dict.lookupScoped<scalar>("rHub", true, false),
            dict.lookupScoped<scalar>("rTip", true, false),
            dict.lookupScoped<scalar>("rFreestream", true, false)
        });

        // Create points for the blade aligned with the X-axis
        pointField points(4, point(0, 0, -dict.lookupScoped<scalar>("halfDepth", true, false)));
        points.replace(0, -rs);

        // Create equivalent points for other blades by rotating
        for (label i = 1; i < dict.lookupScoped<label>("nBlades", true, false); i ++)
        {
            points.append
            (
                transform
                (
                    Rz(degToRad(i*360/scalar(dict.lookupScoped<label>("nBlades", true, false)))),
                    SubField<point>(points, 4)
                )
            );
        }

        // Add the points on the other side of the slab
        points.append(points + vector(0, 0, 2*dict.lookupScoped<scalar>("halfDepth", true, false)));

        // Write out
        os  << points;
//}}} end code
    }
}


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

} // End namespace Foam

// ************************************************************************* //

